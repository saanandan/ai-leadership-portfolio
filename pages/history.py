import base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import date, timedelta, datetime
import anthropic

from database import (
    get_all_engineers,
    get_signals,
    get_all_metrics,
    get_metric_annotations,
    get_active_trend_flags,
    get_annotations_in_range,
    get_blockers_in_range,
    get_all_briefs,
    detect_metric_trends,
    detect_team_wide_patterns,
    save_retrospective,
)
from prompts.retrospective_prompt import build_retrospective_prompt


DELIVERY_EMOJI = {'On Track': '🟢', 'At Risk': '🟡', 'Blocked': '🔴'}
STRESS_EMOJI = {'Low': '🟢', 'Moderate': '🟡', 'High': '🔴'}
UNCERTAINTY_EMOJI = {'Low': '🟢', 'Moderate': '🟡', 'High': '🔴'}
GROWTH_EMOJI = {'Growing': '🌱', 'Coasting': '➡️', 'Struggling': '⚠️'}
CLASS_EMOJI = {'Red': '🔴', 'Orange': '🟠', 'Amber': '⚠️'}
SEVERITY = {'Red': 3, 'Orange': 2, 'Amber': 1}

FLAG_LABELS = {
    'stress_trend': 'Sustained high stress',
    'uncertainty_trend': 'Sustained high uncertainty',
    'delivery_trend': 'Delivery at risk or blocked',
    'energy_trend': 'Low energy pattern',
}


def _fmt_dt(iso_str):
    if not iso_str:
        return ''
    try:
        return datetime.fromisoformat(iso_str).strftime('%b %d, %Y')
    except Exception:
        return iso_str[:10]


def _fmt_dt_long(iso_str):
    if not iso_str:
        return ''
    try:
        return datetime.fromisoformat(iso_str).strftime('%b %d, %Y at %-I:%M %p')
    except Exception:
        return iso_str[:16]


def _parse_dt(iso_str):
    if not iso_str:
        return datetime.min
    try:
        return datetime.fromisoformat(iso_str)
    except Exception:
        try:
            return datetime.strptime(iso_str[:10], '%Y-%m-%d')
        except Exception:
            return datetime.min


def _signal_changes(signals_asc, field):
    """Return rows from chronologically-sorted signals where 'field' value changes."""
    changes = []
    prev = None
    for s in signals_asc:
        val = s[field]
        if val != prev:
            changes.append({'date': s['logged_at'][:10], 'value': val})
            prev = val
    return changes


def _date_range_inputs(start_key, end_key, default_days=30):
    today = date.today()
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Start date", value=today - timedelta(days=default_days), key=start_key)
    with col2:
        end = st.date_input("End date", value=today, max_value=today, key=end_key)
    return start, end


# ── Tab 1 ─────────────────────────────────────────────────────────────────────

def _show_team_history():
    st.markdown("## Team History")
    st.markdown("All activity in the selected period in chronological order.")

    start, end = _date_range_inputs("th_start", "th_end")
    if start > end:
        st.error("❌ Start date must be before end date.")
        return

    st.markdown("---")

    signals = get_signals(start_date=start, end_date=end)
    annotations = get_annotations_in_range(start, end)
    blockers = get_blockers_in_range(start, end)

    all_briefs = get_all_briefs()
    briefs = [
        b for b in all_briefs
        if b.get('generated_at') and start <= date.fromisoformat(b['generated_at'][:10]) <= end
    ]

    # Build unified chronological list
    items = []
    for s in signals:
        items.append({'sort_key': _parse_dt(s['logged_at']), 'type': 'Signal', 'data': s})
    for a in annotations:
        items.append({'sort_key': _parse_dt(a['annotated_at']), 'type': 'Annotation', 'data': a})
    for b in blockers:
        items.append({'sort_key': _parse_dt(b['open_since']), 'type': 'Blocker', 'data': b})
    for b in briefs:
        items.append({'sort_key': _parse_dt(b['generated_at']), 'type': 'Brief', 'data': b})

    items.sort(key=lambda x: x['sort_key'])

    if not items:
        st.info("No activity found in this date range.")
        return

    st.caption(
        f"{len(items)} items — "
        f"{len(signals)} signals · "
        f"{len(annotations)} annotations · "
        f"{len(blockers)} blockers · "
        f"{len(briefs)} briefs"
    )

    for item in items:
        t = item['type']
        d = item['data']

        with st.container(border=True):
            if t == 'Signal':
                st.markdown(
                    f"📝 **Signal** · {_fmt_dt(d['logged_at'])} · **{d['engineer_name']}**"
                )
                st.caption(
                    f"Energy {d['energy_level']}/5 · "
                    f"{DELIVERY_EMOJI.get(d['delivery_signal'], '')} {d['delivery_signal']} · "
                    f"{GROWTH_EMOJI.get(d['growth_signal'], '')} {d['growth_signal']} · "
                    f"Stress {STRESS_EMOJI.get(d['stress_level'], '')} {d['stress_level']} · "
                    f"Uncertainty {UNCERTAINTY_EMOJI.get(d['uncertainty_level'], '')} {d['uncertainty_level']}"
                )
                if d.get('observation'):
                    st.caption(f"Observation: {d['observation']}")

            elif t == 'Annotation':
                emoji = CLASS_EMOJI.get(d['classification'], '')
                st.markdown(
                    f"📊 **Metric Annotation** · {_fmt_dt(d['annotated_at'])} · "
                    f"**{d['metric_name']}** {emoji} {d['classification']}"
                )
                st.caption(f"Value: {d['current_value']}")
                if d.get('explanation'):
                    st.caption(d['explanation'][:200])

            elif t == 'Blocker':
                status = "✅ Resolved" if d.get('resolved') else "🔴 Active"
                st.markdown(
                    f"🚧 **Manager Blocker** · {_fmt_dt(d['open_since'])} · {status}"
                )
                st.caption(d['description'])
                st.caption(f"Escalation: {d['escalation_type']}")

            elif t == 'Brief':
                period = f"{_fmt_dt(d['period_start'])} — {_fmt_dt(d['period_end'])}"
                st.markdown(
                    f"📋 **Leadership Brief** · {_fmt_dt(d['generated_at'])} · Period: {period}"
                )
                display = d['edited_content'] or d['generated_content']
                preview = display[:200].rstrip() + ('...' if len(display) > 200 else '')
                st.caption(preview)


# ── Tab 2 ─────────────────────────────────────────────────────────────────────

def _show_engineer_history():
    st.markdown("## Engineer History")

    engineers = get_all_engineers()
    if not engineers:
        st.info("No engineers found. Add engineers in Team Setup.")
        return

    selected = st.selectbox(
        "Select engineer",
        options=engineers,
        format_func=lambda e: e['name'],
        key="eng_hist_select",
    )

    st.markdown("---")

    signals = get_signals(engineer_id=selected['id'])

    if not signals:
        st.info(f"No signals logged for {selected['name']} yet.")
        return

    signals_asc = sorted(signals, key=lambda s: s['logged_at'])

    st.caption(f"{len(signals)} signals for {selected['name']}")

    # Energy line chart
    st.markdown("### Energy Level Over Time")
    chart_df = pd.DataFrame(
        {'Energy Level': [s['energy_level'] for s in signals_asc]},
        index=[s['logged_at'][:10] for s in signals_asc],
    )
    st.line_chart(chart_df)
    st.caption("Scale: 1 = Depleted, 5 = Highly energized")

    # Delivery timeline
    st.markdown("### Delivery Signal Timeline")
    delivery_changes = _signal_changes(signals_asc, 'delivery_signal')
    if delivery_changes:
        for row in delivery_changes:
            emoji = DELIVERY_EMOJI.get(row['value'], '')
            st.markdown(f"- {row['date']} — {emoji} **{row['value']}**")
    else:
        st.caption("No delivery data recorded.")

    # Stress timeline
    st.markdown("### Stress Level Timeline")
    stress_changes = _signal_changes(signals_asc, 'stress_level')
    if stress_changes:
        for row in stress_changes:
            emoji = STRESS_EMOJI.get(row['value'], '')
            st.markdown(f"- {row['date']} — {emoji} **{row['value']}**")
    else:
        st.caption("No stress data recorded.")

    # Uncertainty timeline
    st.markdown("### Uncertainty Level Timeline")
    uncertainty_changes = _signal_changes(signals_asc, 'uncertainty_level')
    if uncertainty_changes:
        for row in uncertainty_changes:
            emoji = UNCERTAINTY_EMOJI.get(row['value'], '')
            st.markdown(f"- {row['date']} — {emoji} **{row['value']}**")
    else:
        st.caption("No uncertainty data recorded.")

    # Full signal log
    st.markdown("---")
    st.markdown("### All Signals (most recent first)")
    for s in signals:
        with st.container(border=True):
            st.caption(_fmt_dt_long(s['logged_at']))
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Energy", f"{s['energy_level']}/5")
            c2.metric("Delivery", s['delivery_signal'])
            c3.metric("Growth", s['growth_signal'])
            c4.metric("Stress", s['stress_level'])
            c5.metric("Uncertainty", s['uncertainty_level'])
            if s.get('observation'):
                st.caption(f"Observation: {s['observation']}")


# ── Tab 3 ─────────────────────────────────────────────────────────────────────

def _show_metric_history():
    st.markdown("## Metric History")

    metrics = get_all_metrics()
    if not metrics:
        st.info("No active metrics. Add metrics in Metric Management.")
        return

    selected = st.selectbox(
        "Select metric",
        options=metrics,
        format_func=lambda m: m['name'],
        key="metric_hist_select",
    )

    st.markdown("---")

    annotations = get_metric_annotations(selected['id'])

    if not annotations:
        st.info(f"No annotations logged for {selected['name']} yet.")
        return

    st.caption(f"{len(annotations)} annotations for {selected['name']}")

    # Classification progression chart
    st.markdown("### Classification Progression Over Time")
    annotations_asc = sorted(annotations, key=lambda a: a['annotated_at'])
    severity_scores = [SEVERITY.get(a['classification'], 0) for a in annotations_asc]

    chart_df = pd.DataFrame(
        {'Severity': severity_scores},
        index=[a['annotated_at'][:10] for a in annotations_asc],
    )
    st.line_chart(chart_df)
    st.caption("Severity: 3 = Red, 2 = Orange, 1 = Amber — lower score means improving health")

    # Trend summary
    if len(severity_scores) >= 2:
        first_sev = severity_scores[0]
        last_sev = severity_scores[-1]
        if last_sev < first_sev:
            st.success("↗ Improving — trending toward a lower severity classification")
        elif last_sev > first_sev:
            st.warning("↘ Worsening — trending toward a higher severity classification")
        else:
            st.info("→ Stable — classification unchanged over time")

    # All annotations in reverse chronological order
    st.markdown("---")
    st.markdown("### All Annotations (most recent first)")

    for ann in annotations:
        cls = ann['classification']
        emoji = CLASS_EMOJI.get(cls, '')

        with st.container(border=True):
            h_col, d_col = st.columns([3, 2])
            with h_col:
                st.markdown(f"{emoji} **{cls}** — {ann['current_value']}")
                st.caption(_fmt_dt_long(ann['annotated_at']))
            with d_col:
                if ann.get('remediation_owner_name'):
                    st.caption(f"Owner: {ann['remediation_owner_name']}")
                if ann.get('expected_resolution_date'):
                    st.caption(f"Expected resolution: {ann['expected_resolution_date']}")
            st.markdown(ann['explanation'])


# ── Tab 4 ─────────────────────────────────────────────────────────────────────

def _show_team_aggregate():
    st.markdown("## Team Aggregate")
    st.markdown("Signal health summary across the entire team for the selected period.")

    start, end = _date_range_inputs("ta_start", "ta_end")
    if start > end:
        st.error("❌ Start date must be before end date.")
        return

    st.markdown("---")

    signals = get_signals(start_date=start, end_date=end)

    if not signals:
        st.info("No signals in this date range.")
    else:
        engineers_in_period = set(s['engineer_name'] for s in signals)
        st.caption(
            f"{len(signals)} signals from {len(engineers_in_period)} engineers "
            f"({_fmt_dt(str(start))} — {_fmt_dt(str(end))})"
        )

        # Aggregate counts
        delivery_counts = {}
        stress_counts = {}
        uncertainty_counts = {}
        growth_counts = {}
        for s in signals:
            delivery_counts[s['delivery_signal']] = delivery_counts.get(s['delivery_signal'], 0) + 1
            stress_counts[s['stress_level']] = stress_counts.get(s['stress_level'], 0) + 1
            uncertainty_counts[s['uncertainty_level']] = uncertainty_counts.get(s['uncertainty_level'], 0) + 1
            growth_counts[s['growth_signal']] = growth_counts.get(s['growth_signal'], 0) + 1

        avg_energy = sum(s['energy_level'] for s in signals) / len(signals)
        blocked = delivery_counts.get('Blocked', 0)
        at_risk = delivery_counts.get('At Risk', 0)
        high_stress = stress_counts.get('High', 0)
        high_uncertainty = uncertainty_counts.get('High', 0)

        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Avg Energy", f"{avg_energy:.1f}/5")
        m2.metric("Blocked / At Risk", f"{blocked} / {at_risk}")
        m3.metric("High Stress", f"{high_stress} ({round(high_stress / len(signals) * 100)}%)")
        m4.metric("High Uncertainty", f"{high_uncertainty} ({round(high_uncertainty / len(signals) * 100)}%)")

        st.markdown("---")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("#### Delivery")
            for status in ['On Track', 'At Risk', 'Blocked']:
                count = delivery_counts.get(status, 0)
                pct = round(count / len(signals) * 100)
                st.caption(f"{DELIVERY_EMOJI.get(status, '')} {status}: {count} ({pct}%)")

        with col_b:
            st.markdown("#### Stress")
            for level in ['Low', 'Moderate', 'High']:
                count = stress_counts.get(level, 0)
                pct = round(count / len(signals) * 100)
                st.caption(f"{STRESS_EMOJI.get(level, '')} {level}: {count} ({pct}%)")

        with col_c:
            st.markdown("#### Uncertainty")
            for level in ['Low', 'Moderate', 'High']:
                count = uncertainty_counts.get(level, 0)
                pct = round(count / len(signals) * 100)
                st.caption(f"{UNCERTAINTY_EMOJI.get(level, '')} {level}: {count} ({pct}%)")

        st.markdown("#### Growth")
        for status in ['Growing', 'Coasting', 'Struggling']:
            count = growth_counts.get(status, 0)
            pct = round(count / len(signals) * 100)
            st.caption(f"{GROWTH_EMOJI.get(status, '')} {status}: {count} ({pct}%)")

    # Active trend flags — always shown regardless of date filter
    st.markdown("---")
    st.markdown("#### Engineers with Active Trend Flags")

    trend_flags = get_active_trend_flags()

    if not trend_flags:
        st.success("✅ No active trend flags — all engineers within normal patterns.")
    else:
        by_engineer = {}
        for flag in trend_flags:
            name = flag['engineer_name']
            by_engineer.setdefault(name, []).append(flag)

        for name, flags in by_engineer.items():
            with st.container(border=True):
                st.markdown(f"**{name}**")
                for flag in flags:
                    label = FLAG_LABELS.get(flag['flag_type'], flag['flag_type'])
                    st.caption(f"⚠️ {label} — {flag['duration']} consecutive check-ins")


RETRO_SYSTEM_PROMPT = """You are an expert engineering leadership coach helping a manager write a thoughtful retrospective on their team's performance over time.

Your job is to turn historical team signal data into a narrative retrospective summary that tells the story of how the team evolved during the period. This retrospective should help the manager understand the arc of team health, articulate patterns for performance conversations, and prepare for quarterly business reviews.

Write in a reflective, narrative tone. Go beyond listing facts — connect the dots, explain what the data suggests, and help the manager understand the story behind the numbers. Be specific: name engineers, name metrics, describe how things changed over time.

Be honest about challenges while recognizing what went well. A good retrospective holds both clearly."""


def _retro_copy_button(text: str):
    """Render a Copy to Clipboard button for the retrospective text area."""
    if not text:
        return
    encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
    components.html(
        f"""
        <script>
        async function doCopy() {{
            const raw = atob('{encoded}');
            const bytes = Uint8Array.from(raw, c => c.charCodeAt(0));
            const decoded = new TextDecoder('utf-8').decode(bytes);
            const btn = document.getElementById('retrocpbtn');
            try {{
                await navigator.clipboard.writeText(decoded);
                btn.textContent = '✅ Copied!';
            }} catch (_) {{
                const ta = document.createElement('textarea');
                ta.value = decoded;
                ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                try {{
                    document.execCommand('copy');
                    btn.textContent = '✅ Copied!';
                }} catch (_2) {{
                    btn.textContent = '❌ Copy failed — select and copy manually';
                }}
                document.body.removeChild(ta);
            }}
            setTimeout(() => btn.textContent = '\U0001f4cb Copy to Clipboard', 2000);
        }}
        </script>
        <button id="retrocpbtn" onclick="doCopy()" style="
            background: #1f77b4;
            color: #ffffff;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-family: sans-serif;
        ">\U0001f4cb Copy to Clipboard</button>
        """,
        height=50,
    )


# ── Tab 5: Retrospective ──────────────────────────────────────────────────────

def _show_retrospective():
    st.markdown("## Retrospective Summary")
    st.markdown(
        "Generate a narrative summary of how your team evolved over a period. "
        "Use this for quarterly business reviews, performance conversations, or your own reflection."
    )

    today = date.today()
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Start date", value=today - timedelta(days=90), key="retro_start")
    with col2:
        end = st.date_input("End date", value=today, max_value=today, key="retro_end")

    if start > end:
        st.error("❌ Start date must be before end date.")
        return

    st.markdown("---")

    if st.button("Generate Retrospective Summary", type="primary"):
        st.session_state.retro_error = None
        st.session_state.retro_save_status = None
        with st.spinner("Generating retrospective summary..."):
            try:
                data = {
                    'period_start': str(start),
                    'period_end': str(end),
                    'signals': get_signals(start_date=start, end_date=end),
                    'annotations': get_annotations_in_range(start, end),
                    'blockers': get_blockers_in_range(start, end),
                    'trend_flags': get_active_trend_flags(),
                    'metric_trend_flags': detect_metric_trends(),
                    'team_wide_patterns': detect_team_wide_patterns(),
                }

                prompt = build_retrospective_prompt(data)

                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=4096,
                    system=[{
                        "type": "text",
                        "text": RETRO_SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text

                # Store content and period — do NOT save to DB yet
                st.session_state.retro_content = content
                st.session_state['retro_text_area'] = content
                st.session_state.retro_period_start = str(start)
                st.session_state.retro_period_end = str(end)

            except anthropic.AuthenticationError:
                st.session_state.retro_error = (
                    "Authentication failed. Please check that the ANTHROPIC_API_KEY "
                    "environment variable is set correctly."
                )
            except anthropic.RateLimitError:
                st.session_state.retro_error = (
                    "Rate limit reached. Please wait a moment and try again."
                )
            except anthropic.APIConnectionError:
                st.session_state.retro_error = (
                    "Could not connect to the Anthropic API. "
                    "Please check your internet connection and try again."
                )
            except Exception as e:
                st.session_state.retro_error = f"An unexpected error occurred: {e}"

    if st.session_state.get('retro_error'):
        st.error(f"❌ {st.session_state.retro_error}")

    if st.session_state.get('retro_content'):
        st.markdown("---")
        st.markdown("### Generated Retrospective")

        # Editable text area — value managed via session state key
        st.text_area(
            "Retrospective",
            height=700,
            key="retro_text_area",
            label_visibility="collapsed",
        )

        st.caption(
            "Review and edit the retrospective before saving. "
            "Use Save Retrospective when you are satisfied with the content."
        )

        # Save and Copy buttons
        btn_col, copy_col, _ = st.columns([1, 1, 3])

        with btn_col:
            if st.button("Save Retrospective", type="primary"):
                current_text = st.session_state.get('retro_text_area') or st.session_state.retro_content
                period_start = st.session_state.get('retro_period_start')
                period_end = st.session_state.get('retro_period_end')
                if current_text and period_start and period_end:
                    rid = save_retrospective(period_start, period_end, current_text)
                    if rid:
                        st.session_state.retro_save_status = 'saved'
                    else:
                        st.session_state.retro_save_status = 'error'
                    st.rerun()

        with copy_col:
            current_text = st.session_state.get('retro_text_area') or st.session_state.retro_content
            _retro_copy_button(current_text)

        if st.session_state.get('retro_save_status') == 'saved':
            st.success("✅ Retrospective saved.")
        elif st.session_state.get('retro_save_status') == 'error':
            st.error("❌ Failed to save. Please try again.")

        st.caption(
            "Use this for quarterly business reviews, performance conversations, "
            "or your own reflection on how the team has evolved."
        )

    elif not st.session_state.get('retro_error'):
        st.info(
            "Select a date range covering the period you want to reflect on — "
            "typically the last 90 days for a quarterly retrospective."
        )


# ── Entry point ───────────────────────────────────────────────────────────────

def show_history():
    st.set_page_config(
        page_title="History - Engineering Leadership Signal Tool",
        page_icon="📈",
        layout="wide",
    )

    # Session state for retrospective
    for key, default in [
        ('retro_content', None),
        ('retro_error', None),
        ('retro_save_status', None),
        ('retro_period_start', None),
        ('retro_period_end', None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    st.markdown("# 📈 History")
    st.markdown("Browse past signals, annotations, blockers, and briefs.")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗓️ Team History",
        "👤 Engineer History",
        "📊 Metric History",
        "📉 Team Aggregate",
        "📜 Retrospective",
    ])

    with tab1:
        _show_team_history()

    with tab2:
        _show_engineer_history()

    with tab3:
        _show_metric_history()

    with tab4:
        _show_team_aggregate()

    with tab5:
        _show_retrospective()


if __name__ == "__main__":
    show_history()

from datetime import datetime


FLAG_LABELS = {
    'stress_trend': 'Sustained high stress',
    'uncertainty_trend': 'Sustained high uncertainty',
    'delivery_trend': 'Delivery at risk or blocked',
    'energy_trend': 'Low energy pattern',
    'sustained_red': 'Metric sustained red',
    'improving_trend': 'Metric improving',
    'sustained_improvement': 'Metric sustained improvement',
    'stress_pattern': 'Team-wide high stress',
    'uncertainty_pattern': 'Team-wide high uncertainty',
}


def _fmt(iso_str):
    if not iso_str:
        return ''
    try:
        return datetime.fromisoformat(iso_str).strftime('%b %d, %Y')
    except Exception:
        return iso_str[:10]


def build_retrospective_prompt(data):
    """Build the user prompt for Claude to generate a team retrospective."""
    period_start = data.get('period_start', '')
    period_end = data.get('period_end', '')
    signals = data.get('signals', [])
    annotations = data.get('annotations', [])
    blockers = data.get('blockers', [])
    trend_flags = data.get('trend_flags', [])
    metric_trend_flags = data.get('metric_trend_flags', [])
    team_wide_patterns = data.get('team_wide_patterns', [])

    sections = []

    # ── Section 1: Signals grouped by engineer, chronological ─────────────────
    if signals:
        by_engineer = {}
        for s in sorted(signals, key=lambda x: x['logged_at']):
            by_engineer.setdefault(s['engineer_name'], []).append(s)

        lines = [f"ENGINEER SIGNAL HISTORY ({_fmt(str(period_start))} — {_fmt(str(period_end))}):"]
        for name, eng_signals in by_engineer.items():
            lines.append(f"\n{name}:")
            for s in eng_signals:
                stress_note = f" (source: {s['stress_source']})" if s.get('stress_source') else ''
                uncertainty_note = f" (source: {s['uncertainty_source']})" if s.get('uncertainty_source') else ''
                obs = f" | Observation: {s['observation']}" if s.get('observation') else ''
                lines.append(
                    f"  - {_fmt(s['logged_at'])}: "
                    f"Energy={s['energy_level']}/5, "
                    f"Delivery={s['delivery_signal']}, "
                    f"Growth={s['growth_signal']}, "
                    f"Stress={s['stress_level']}{stress_note}, "
                    f"Uncertainty={s['uncertainty_level']}{uncertainty_note}{obs}"
                )
        sections.append('\n'.join(lines))
    else:
        sections.append(
            f"ENGINEER SIGNAL HISTORY:\nNo signals logged for this period ({_fmt(str(period_start))} — {_fmt(str(period_end))})."
        )

    # ── Section 2: Annotations grouped by metric, chronological ───────────────
    if annotations:
        by_metric = {}
        for a in sorted(annotations, key=lambda x: x['annotated_at']):
            by_metric.setdefault(a['metric_name'], []).append(a)

        lines = ["METRIC ANNOTATION HISTORY (chronological per metric):"]
        for metric_name, anns in by_metric.items():
            lines.append(f"\n{metric_name}:")
            for a in anns:
                owner = f", Owner: {a['remediation_owner_name']}" if a.get('remediation_owner_name') else ''
                resolution = f", Expected resolution: {a['expected_resolution_date']}" if a.get('expected_resolution_date') else ''
                lines.append(
                    f"  - {_fmt(a['annotated_at'])}: [{a['classification']}] {a['current_value']}{owner}{resolution}"
                    f" — \"{a['explanation']}\""
                )
        sections.append('\n'.join(lines))
    else:
        sections.append("METRIC ANNOTATION HISTORY:\nNo metric annotations in this period.")

    # ── Section 3: Blockers with resolution status ─────────────────────────────
    if blockers:
        lines = ["BLOCKERS IN THIS PERIOD:"]
        for b in sorted(blockers, key=lambda x: x['open_since']):
            if b.get('resolved'):
                resolution = f"RESOLVED {_fmt(b.get('resolved_at', ''))}: \"{b.get('resolution_description', '')}\""
            else:
                resolution = "STILL ACTIVE"
            lines.append(
                f"- \"{b['description']}\" — opened {_fmt(b['open_since'])}, "
                f"Escalation: {b['escalation_type']}, Ask: {b['specific_ask']} | {resolution}"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("BLOCKERS IN THIS PERIOD:\nNo blockers opened in this period.")

    # ── Section 4: Engineer trend flags ───────────────────────────────────────
    if trend_flags:
        lines = ["ACTIVE ENGINEER TREND FLAGS:"]
        for flag in trend_flags:
            label = FLAG_LABELS.get(flag['flag_type'], flag['flag_type'])
            lines.append(f"- {flag['engineer_name']}: {label} ({flag['duration']} consecutive check-ins)")
        sections.append('\n'.join(lines))
    else:
        sections.append("ACTIVE ENGINEER TREND FLAGS:\nNone.")

    # ── Section 5: Metric trend flags ─────────────────────────────────────────
    if metric_trend_flags:
        lines = ["ACTIVE METRIC TREND FLAGS:"]
        for flag in metric_trend_flags:
            label = FLAG_LABELS.get(flag['flag_type'], flag['flag_type'])
            lines.append(f"- {flag['metric_name']}: {label} ({flag['duration']} consecutive annotations)")
        sections.append('\n'.join(lines))
    else:
        sections.append("ACTIVE METRIC TREND FLAGS:\nNone.")

    # ── Section 6: Team-wide patterns ─────────────────────────────────────────
    if team_wide_patterns:
        lines = ["TEAM-WIDE PATTERNS:"]
        for p in team_wide_patterns:
            label = FLAG_LABELS.get(p['pattern_type'], p['pattern_type'])
            source = f" (most common source: {p['most_common_source']})" if p.get('most_common_source') else ''
            lines.append(
                f"- {label}: {p['affected_count']} of {p['total_engineers']} engineers "
                f"for {p['duration_weeks']} consecutive weeks{source}"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("TEAM-WIDE PATTERNS:\nNone detected.")

    data_block = '\n\n'.join(sections)

    start_label = _fmt(str(period_start))
    end_label = _fmt(str(period_end))

    prompt = f"""Below is historical team signal data for the period {start_label} to {end_label}. Use it to write a team retrospective summary.

---

{data_block}

---

Write a retrospective summary for the period {start_label} to {end_label} with exactly these 7 sections in order. Use markdown headers (##). Write in reflective, narrative prose — not just bullet lists. Be specific: name engineers, name metrics, describe how things changed over time. Do not invent information not present in the data.

## 1. Team Health Evolution
Describe how the team's overall health changed across the period. Reference the signal data — energy trends, delivery patterns, stress and uncertainty arcs. What was the overall trajectory?

## 2. Consistent Strength
Which engineers showed consistent positive signals across the period? What did they do well? Cite specific signals and patterns.

## 3. Sustained Risk Signals
Which engineers showed sustained risk signals — repeated low energy, elevated stress, delivery blocks, or uncertainty? What does the data suggest about their situation? Reference specific trend flags if present.

## 4. Operational Metrics Trends
How did operational metrics move during this period? For each annotated metric, describe whether it improved, worsened, or stayed flat. Call out metrics that were persistently red and those that improved.

## 5. Team-Wide Patterns
What team-wide patterns were detected, if any? What do they suggest about systemic issues — workload, direction, management communication? Be direct about what the patterns indicate.

## 6. Blockers and Resolution
What manager blockers were open during this period? Were they resolved? How long were they open? If any remain active, note that they are still outstanding.

## 7. Reflection and Outlook
What are the most important things the manager should take from this period — what worked, what didn't, and what needs attention going forward?
"""

    return prompt

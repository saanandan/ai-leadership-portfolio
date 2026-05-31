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


def _fmt_date(iso_str):
    if not iso_str:
        return ''
    try:
        return datetime.fromisoformat(iso_str).strftime('%b %d, %Y')
    except Exception:
        return iso_str


def build_brief_prompt(data):
    """Build the user prompt for Claude from aggregated brief data."""
    signals = data.get('signals', [])
    metric_annotations = data.get('metric_annotations', [])
    trend_flags = data.get('trend_flags', [])
    metric_trend_flags = data.get('metric_trend_flags', [])
    active_blockers = data.get('active_blockers', [])
    aging_blocker_ids = data.get('aging_blocker_ids', set())
    team_wide_patterns = data.get('team_wide_patterns', [])

    sections = []

    # ── Section 1: Signal summary ─────────────────────────────────────────────
    if signals:
        lines = ["SIGNALS LOGGED IN THIS PERIOD:"]
        for s in signals:
            logged = _fmt_date(s.get('logged_at', ''))
            stress_detail = f" (source: {s['stress_source']})" if s.get('stress_source') else ''
            uncertainty_detail = f" (source: {s['uncertainty_source']})" if s.get('uncertainty_source') else ''
            obs = f" Observation: {s['observation']}" if s.get('observation') else ''
            lines.append(
                f"- {s['engineer_name']} on {logged}: "
                f"Energy={s['energy_level']}/5, "
                f"Delivery={s['delivery_signal']}, "
                f"Growth={s['growth_signal']}, "
                f"Stress={s['stress_level']}{stress_detail}, "
                f"Uncertainty={s['uncertainty_level']}{uncertainty_detail}."
                f"{obs}"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("SIGNALS LOGGED IN THIS PERIOD:\nNo signals logged in this date range.")

    # ── Section 2: Metric annotations ─────────────────────────────────────────
    if metric_annotations:
        lines = ["METRIC ANNOTATIONS (most recent per metric):"]
        for ann in metric_annotations:
            annotated = _fmt_date(ann.get('annotated_at', ''))
            owner = f", Owner: {ann['remediation_owner_name']}" if ann.get('remediation_owner_name') else ''
            resolution = f", Expected resolution: {ann['expected_resolution_date']}" if ann.get('expected_resolution_date') else ''
            context = f" Strategic context: {ann['strategic_context']}" if ann.get('strategic_context') else ''
            lines.append(
                f"- {ann['metric_name']} [{ann['classification']}] = {ann['current_value']} "
                f"(annotated {annotated}{owner}{resolution}). "
                f"Explanation: {ann['explanation']}{context}"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("METRIC ANNOTATIONS:\nNo metric annotations on record.")

    # ── Section 3: Engineer trend flags ───────────────────────────────────────
    if trend_flags:
        lines = ["ENGINEER TREND FLAGS (active patterns):"]
        for flag in trend_flags:
            label = FLAG_LABELS.get(flag['flag_type'], flag['flag_type'])
            lines.append(f"- {flag['engineer_name']}: {label} ({flag['duration']} consecutive check-ins)")
        sections.append('\n'.join(lines))
    else:
        sections.append("ENGINEER TREND FLAGS:\nNo active engineer trend flags.")

    # ── Section 4: Metric trend flags ─────────────────────────────────────────
    if metric_trend_flags:
        lines = ["METRIC TREND FLAGS (active patterns):"]
        for flag in metric_trend_flags:
            label = FLAG_LABELS.get(flag['flag_type'], flag['flag_type'])
            lines.append(f"- {flag['metric_name']}: {label} ({flag['duration']} consecutive annotations)")
        sections.append('\n'.join(lines))
    else:
        sections.append("METRIC TREND FLAGS:\nNo active metric trend flags.")

    # ── Section 5: Active blockers ────────────────────────────────────────────
    if active_blockers:
        lines = ["ACTIVE MANAGER BLOCKERS:"]
        for blocker in active_blockers:
            aging = ' [AGING - 14+ days]' if blocker['id'] in aging_blocker_ids else ''
            lines.append(
                f"- {blocker['description']}{aging} "
                f"(open since {blocker['open_since']}, "
                f"escalation: {blocker['escalation_type']}). "
                f"Ask: {blocker['specific_ask']}"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("ACTIVE MANAGER BLOCKERS:\nNo active blockers.")

    # ── Section 6: Team-wide patterns ─────────────────────────────────────────
    if team_wide_patterns:
        lines = ["TEAM-WIDE PATTERN ALERTS:"]
        for pattern in team_wide_patterns:
            label = FLAG_LABELS.get(pattern['pattern_type'], pattern['pattern_type'])
            source_note = f" (most common source: {pattern['most_common_source']})" if pattern.get('most_common_source') else ''
            lines.append(
                f"- {label}: {pattern['affected_count']} of {pattern['total_engineers']} engineers "
                f"for {pattern['duration_weeks']} consecutive weeks{source_note}"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("TEAM-WIDE PATTERN ALERTS:\nNo team-wide patterns detected.")

    data_block = '\n\n'.join(sections)

    prompt = f"""Below is the aggregated data from the Engineering Leadership Signal Tool for this period. Use it to generate a structured leadership brief.

---

{data_block}

---

Generate a leadership brief using the exact structure below. Use markdown headers (##) for each section. Keep the entire brief readable in under 3 minutes — use bullet points not paragraphs, and be direct and factual. Do not invent information not present in the data above.

## Director Summary
Exactly three bullet points. Each bullet is one sentence maximum — no run-on sentences. Plain English, no jargon. Lead with metrics and blockers; people are important context but not the headline.
- 🔴 **Needs your attention:** the single most urgent issue — lead with a metric that is a genuine problem if one exists, otherwise an aging blocker, otherwise a person at retention risk
- 🟠 **Watch list:** the most important thing being actively managed — lead with a metric leadership should be aware of if one exists, otherwise a blocker in progress, otherwise a person showing early warning signs
- ✅ **On track:** the most notable positive — lead with a metric improving if one exists, otherwise a blocker resolved, otherwise a person performing well

## Needs Leadership Escalation
Issues outside the manager's control that require director or above intervention. Use bullet points, in this order:
- Metrics with genuine issues caused by external factors (dependency failures, retroactive policy changes) — lead each with a one-sentence plain English verdict
- Aging blockers requiring escalation — include the specific ask
- People at retention risk who need skip-level awareness

If nothing requires escalation, say so in one line.

## Manager Has a Handle On It
Issues being actively managed within the team's control. Use bullet points, in this order:
- Metrics that are Red or Orange but improving with a clear plan — lead each with a one-sentence plain English verdict
- Blockers being actively worked by the manager
- Individual engineer trends being monitored and addressed

If nothing is in this category, say so in one line.

## On Track
Things going well that deserve recognition. Use bullet points, in this order:
- Metrics showing sustained improvement or a clear positive trajectory
- No active blocker issues (note this if true)
- Engineers performing strongly — wins and bright spots worth calling out

## Manager Actions
A prioritized bullet list of specific actions the manager should take in the next 1-2 weeks. Be concrete — name the person, name the action.

## Looking Ahead
1-2 sentences on what to watch closely in the coming period given current trends and open items.
"""

    return prompt

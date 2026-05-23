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
            lines.append(
                f"- {label}: {pattern['affected_count']} of {pattern['team_size']} engineers "
                f"({pattern['percentage']}%) over the last {pattern['duration_weeks']} weeks"
            )
        sections.append('\n'.join(lines))
    else:
        sections.append("TEAM-WIDE PATTERN ALERTS:\nNo team-wide patterns detected.")

    data_block = '\n\n'.join(sections)

    prompt = f"""Below is the aggregated data from the Engineering Leadership Signal Tool for this period. Use it to generate a structured leadership brief.

---

{data_block}

---

Generate a leadership brief with exactly these 8 sections in order. Use markdown headers (##) for each section. Be direct, factual, and solution-oriented. Mix short narrative with bullet points where appropriate. Do not invent information — if data is missing for a section, say so briefly.

## 1. Team Overview
A 2-3 sentence summary of overall team health this period based on energy levels, delivery signals, and growth signals.

## 2. Delivery Status
Who is on track, who is at risk, and who is blocked. Include any delivery trend flags. Note if anyone needs immediate attention.

## 3. Operational Metrics
Summarize the current state of each annotated metric. Distinguish between genuine problems (Red), contextual issues (Orange), and temporary dips (Amber). Include expected resolution dates where set.

## 4. Trends Requiring Attention
List any active trend flags for engineers or metrics that need management action. For each trend, suggest a concrete next step.

## 5. Bright Spots
What is going well? Highlight positive signals, improving metrics, engineers showing growth, engineers on track.

## 6. Manager Blockers
List all active blockers needing manager involvement. Flag any aging blockers (14+ days). State the specific ask for each.

## 7. Manager Actions
A prioritized list of specific actions the manager should take in the next 1-2 weeks based on everything above. Be concrete and actionable.

## 8. Looking Ahead
1-2 sentences on what to watch closely in the coming period given current trends and open items.
"""

    return prompt

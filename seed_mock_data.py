#!/usr/bin/env python3
"""
seed_mock_data.py — Populate the database with realistic mock data for testing/demos.

    python seed_mock_data.py
"""
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from database import initialize_database, get_connection

# ── Reference date ────────────────────────────────────────────────────────────
TODAY = date(2026, 5, 23)

# 8 Monday-anchored weeks, oldest → newest
SIGNAL_WEEKS = [TODAY - timedelta(weeks=w) for w in range(7, -1, -1)]

# ── Engineers ─────────────────────────────────────────────────────────────────
ENGINEERS = [
    ("Sarah Chen",     "Senior Associate"),
    ("Marcus Johnson", "Lead Engineer"),
    ("Priya Patel",    "Associate"),
    ("Derek Williams", "Senior Associate"),
    ("Amy Rodriguez",  "Principal Associate"),
    ("James Kim",      "Lead Engineer"),
    ("Lisa Thompson",  "Associate"),
    ("Omar Hassan",    "Senior Associate"),
]

# ── Signal helpers ────────────────────────────────────────────────────────────
def s(energy, delivery, growth, stress, stress_src, uncertainty, unc_src, obs):
    return dict(
        energy_level=energy,
        delivery_signal=delivery,
        growth_signal=growth,
        stress_level=stress,
        stress_source=stress_src,
        uncertainty_level=uncertainty,
        uncertainty_source=unc_src,
        observation=obs,
    )

# ── Signal patterns (8 entries per engineer, oldest → newest) ─────────────────
SIGNAL_DATA = {
    "Sarah Chen": [
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Shipped auth service ahead of schedule."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Strong PR throughput, unblocking teammates."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Led design review; very engaged."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Good velocity; mentoring Priya effectively."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Proactively caught a production regression."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Delivered milestone two days early."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Positive impact on team code quality."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "High output; morale is excellent."),
    ],
    "Marcus Johnson": [
        s(4, "On Track", "Coasting", "Low",  None,                   "Low",  None,                    "Solid delivery but less initiative than usual."),
        s(4, "On Track", "Coasting", "Low",  None,                   "Low",  None,                    "Meeting commitments; energy seems flat."),
        s(3, "On Track", "Coasting", "Low",  None,                   "Low",  None,                    "Slower review turnarounds; flagged workload concerns."),
        s(3, "On Track", "Coasting", "Low",  None,                   "Low",  None,                    "Delivered but disengaged in planning sessions."),
        s(3, "On Track", "Coasting", "High", "Organizational pressure", "Low",  None,                 "Expressed frustration with reorg uncertainty."),
        s(2, "At Risk",  "Coasting", "High", "Organizational pressure", "High", "Reorg direction unclear", "Missing standups; deliverables slipping."),
        s(2, "At Risk",  "Coasting", "High", "Organizational pressure", "High", "Reorg direction unclear", "Continued delivery risk; 1:1 flagged disengagement."),
        s(2, "At Risk",  "Coasting", "High", "Organizational pressure", "High", "Reorg direction unclear", "At risk of missing sprint goal. Needs intervention."),
    ],
    "Priya Patel": [
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Ramping up well; asking good questions."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Consistent output; workload feels heavy but manageable."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Good PRs shipped; flagged ticket backlog as stressor."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Steady progress; pairing with Sarah effectively."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Completed first solo feature end-to-end."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Good momentum; sprint commitment met."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "On track; mentioned feeling stretched but positive."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Continued solid delivery; growth trajectory clear."),
    ],
    "Derek Williams": [
        s(3, "On Track", "Struggling", "Low",  None,           "Low", None, "Inconsistent throughput; needs support."),
        s(3, "On Track", "Struggling", "Low",  None,           "Low", None, "Behind on two tickets; blockers not raised proactively."),
        s(3, "On Track", "Struggling", "Low",  None,           "Low", None, "Sprint goals partially met; engagement low."),
        s(3, "On Track", "Struggling", "Low",  None,           "Low", None, "Output declining; mentioned friction with adjacent team."),
        s(3, "On Track", "Struggling", "Low",  None,           "Low", None, "Missing design reviews; delivery at risk."),
        s(3, "On Track", "Struggling", "High", "Team dynamics", "Low", None, "Raised interpersonal conflict with team member."),
        s(2, "Blocked",  "Struggling", "High", "Team dynamics", "Low", None, "Blocked on cross-team dependency; energy visibly low."),
        s(2, "Blocked",  "Struggling", "High", "Team dynamics", "Low", None, "Still blocked; requested 1:1 to discuss team dynamics."),
    ],
    "Amy Rodriguez": [
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Exceptional — leading architecture initiative."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "High quality output; positive influence on team."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Completed platform upgrade ahead of plan."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Proactively mentoring two junior engineers."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Strong sprint; presented work at all-hands."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Identified and fixed a long-standing reliability issue."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Bright spot — consistent excellence and team uplift."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Delivered major feature; team morale boost."),
    ],
    "James Kim": [
        s(3, "On Track", "Coasting", "Low",      None,                 "Low",  None,                 "Delivering but not stretching beyond scope."),
        s(3, "On Track", "Coasting", "Low",      None,                 "Low",  None,                 "Consistent; seems disengaged from roadmap discussions."),
        s(3, "On Track", "Coasting", "Low",      None,                 "Low",  None,                 "On time delivery; no growth signals observed."),
        s(3, "On Track", "Coasting", "Low",      None,                 "Low",  None,                 "Mentioned confusion about Q3 priorities."),
        s(3, "On Track", "Coasting", "Moderate", "Shifting priorities","Low",  None,                 "Frustrated by repeated priority changes."),
        s(3, "On Track", "Coasting", "Moderate", "Shifting priorities","Low",  None,                 "Delivered but raised concerns about scope creep."),
        s(3, "At Risk",  "Coasting", "Moderate", "Shifting priorities","High", "Unclear Q3 roadmap", "Slipping on commitments; needs roadmap clarity."),
        s(3, "At Risk",  "Coasting", "Moderate", "Shifting priorities","High", "Unclear Q3 roadmap", "At risk; uncertainty about direction affecting output."),
    ],
    "Lisa Thompson": [
        s(3, "On Track", "Growing", "Low", None, "Moderate", "Timeline clarity", "Ramping steadily; some questions about project scope."),
        s(4, "On Track", "Growing", "Low", None, "Moderate", "Timeline clarity", "Strong week; good velocity on assigned tickets."),
        s(2, "On Track", "Growing", "Low", None, "Moderate", "Scope unclear",    "Lower energy this week; personal factors mentioned."),
        s(4, "On Track", "Growing", "Low", None, "Moderate", "Scope unclear",    "Bounced back; solid delivery resumed."),
        s(3, "On Track", "Growing", "Low", None, "Moderate", "Timeline clarity", "Steady output; checking in on roadmap frequently."),
        s(4, "On Track", "Growing", "Low", None, "Moderate", "Timeline clarity", "Good sprint; proactively raising blockers early."),
        s(2, "On Track", "Growing", "Low", None, "Moderate", "Scope unclear",    "Energy dip again; nothing alarming but worth watching."),
        s(3, "On Track", "Growing", "Low", None, "Moderate", "Timeline clarity", "Stable; overall trajectory positive despite fluctuations."),
    ],
    "Omar Hassan": [
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Reliable delivery; consistent pace."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Good output; calm and focused."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Steady progress on maintenance work."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Consistent contributor; team relies on his stability."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "On track; no concerns flagged."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Dependable delivery; good team presence."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Consistent pace; stable energy."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Solid week; steady as always."),
    ],
}

# ── Metric annotations (8 weeks per metric, oldest → newest) ─────────────────
# Each tuple: (current_value, classification, explanation)
ANNOTATION_DATA = {
    "CICD Health": [
        ("65%", "Red",    "Build success rate at 65% — below the 70% threshold. Flaky tests and infra instability driving failures."),
        ("66%", "Red",    "Marginal uptick to 66% but still Red. Root cause analysis in progress; build agent pool suspected."),
        ("68%", "Red",    "Slight improvement to 68% but insufficient. Pipeline reliability work underway by infra team."),
        ("75%", "Orange", "Pipeline optimisations landed — jumped to 75%. Build agent pool resized and flaky tests quarantined."),
        ("76%", "Orange", "Holding at 76%; infrastructure team continuing to stabilise build agents and reduce retry rate."),
        ("83%", "Amber",  "Major improvement to 83% following completion of build agent overhaul and test reliability fixes."),
        ("85%", "Amber",  "Healthy at 85%. Improvement trend sustained. Focus shifting to maintaining gains rather than firefighting."),
        ("87%", "Amber",  "Continuing to improve at 87%. Team now monitoring for regressions; no new flaky tests introduced."),
    ],
    "Vuln Remediation": [
        ("42%", "Red",    "Vuln remediation at 42% — significant backlog of open vulnerabilities across three services."),
        ("44%", "Red",    "Marginal progress at 44%. SLA breaches on 3 critical vulns escalated to security team."),
        ("43%", "Red",    "Slight dip to 43% as new vulns discovered. Security team overwhelmed; capacity issue flagged."),
        ("46%", "Red",    "Back to 46%. Remediation pace not keeping up with new vulnerability discovery rate."),
        ("49%", "Red",    "Approaching 50% threshold. Temporary engineering support allocated from platform team."),
        ("50%", "Red",    "Holding at 50%. Dedicated remediation sprint starting next week to clear backlog."),
        ("60%", "Orange", "Dedicated sprint paying off — jumped to 60%. High-severity vulns cleared; momentum building."),
        ("70%", "Orange", "Strong improvement to 70%. On track to reach Amber threshold within two weeks."),
    ],
    "Deployment Success Rate": [
        ("88%", "Orange", "Deployment success at 88%. Occasional rollbacks from config drift in staging-to-prod promotion."),
        ("89%", "Orange", "89% — stable. Rollback procedure well-practised by on-call rotation; mean-time-to-recovery improving."),
        ("90%", "Orange", "Consistent 90%. Targeting Amber threshold with upcoming canary rollout improvements."),
        ("91%", "Orange", "91% success rate. Feature flagging reducing blast radius of failed deploys significantly."),
        ("90%", "Orange", "Slight dip to 90% after minor regression in canary process. Identified and resolved within 24 hours."),
        ("92%", "Orange", "92% — best week this quarter. Canary fixes fully merged and validated in production."),
        ("91%", "Orange", "91% holding steady. Deploy frequency increased 30% with no corresponding quality drop."),
        ("92%", "Orange", "Strong at 92%. Team is shipping frequently and confidently; deploy automation improvements planned for Q3."),
    ],
    "Test Coverage": [
        ("70%", "Red",    "Coverage dipped to 70% after rapid feature sprint. Below Amber floor; test debt accumulated."),
        ("72%", "Amber",  "Coverage recovered to 72% after dedicated test-writing sprint. Coverage gate added to CI pipeline."),
        ("73%", "Amber",  "73% — incremental improvement. Coverage gate blocking merges below 70% preventing further regression."),
        ("74%", "Amber",  "74%. Steady improvement as team adopts TDD practices for new feature work."),
        ("75%", "Amber",  "75% and rising. New engineers ramping up on test standards with pairing sessions."),
        ("76%", "Amber",  "76% — consistent progress. Coverage improving without meaningfully slowing delivery pace."),
        ("77%", "Amber",  "77% this week. Team morale around testing quality is high; engineers taking pride in coverage."),
        ("78%", "Amber",  "78% — highest this quarter. Approaching target threshold of 80% ahead of Q3 deadline."),
    ],
}

STRATEGIC_CONTEXTS = {
    "CICD Health": (
        "Build reliability is a Q2 OKR — targeting Amber by end of quarter. "
        "Infrastructure team dedicated 40% capacity to pipeline improvements following two prod incidents in Q1."
    ),
    "Vuln Remediation": (
        "Security posture is a board-level priority following the industry-wide vulnerability report in Q1. "
        "Target: reduce open vulnerabilities by 80% this half. Security team added two dedicated remediation engineers."
    ),
    "Deployment Success Rate": (
        "Deploy cadence increased to daily following CI/CD improvements in Q1. "
        "Success rate tracks closely with customer experience SLAs and on-call page volume."
    ),
    "Test Coverage": (
        "80% coverage is the Q3 engineering quality target agreed with VP Engineering. "
        "Coverage gate added to CI in week 3 to prevent regression below 70% floor."
    ),
}

# ── Manager blockers ──────────────────────────────────────────────────────────
BLOCKERS = [
    {
        "description": "Waiting on platform team to unblock API gateway migration for auth service",
        "open_since":  (TODAY - timedelta(weeks=6)).isoformat(),
        "what_tried":  (
            "Escalated to platform team lead directly; filed ticket in their backlog with P1 priority; "
            "attended their sprint planning to advocate for prioritisation"
        ),
        "options_remaining": "None — resolved through escalation path",
        "escalation_type":   "Resource",
        "specific_ask":      "Need platform team to prioritise API gateway migration unblock within this sprint",
        "resolved":           True,
        "resolved_at":       (TODAY - timedelta(weeks=3)).isoformat(),
        "resolution_description": (
            "Platform team completed API gateway configuration changes on schedule. "
            "Auth service migration unblocked and shipped successfully."
        ),
    },
    {
        "description": "Headcount approval pending for senior engineer backfill — role open since last quarter",
        "open_since":  (TODAY - timedelta(weeks=5)).isoformat(),
        "what_tried":  (
            "Submitted HC request via HR portal with full business justification; "
            "followed up with HRBP twice; escalated to skip-level manager three weeks ago"
        ),
        "options_remaining": (
            "Waiting on VP sign-off in next budget review cycle; "
            "exploring contractor bridge option as 60-day fallback to relieve team load"
        ),
        "escalation_type": "Decision",
        "specific_ask":    (
            "Need VP approval for HC request by end of month to hit Q3 hiring target "
            "and avoid sprint capacity shortfall in July"
        ),
        "resolved":           False,
        "resolved_at":        None,
        "resolution_description": None,
    },
    {
        "description": "Architecture decision required: monolith-first vs microservices for new authentication module",
        "open_since":  (TODAY - timedelta(weeks=1)).isoformat(),
        "what_tried":  (
            "Drafted architecture proposal with trade-off analysis; "
            "shared with senior engineers; received conflicting opinions with no consensus"
        ),
        "options_remaining": (
            "Need input from principal architect and CTO to break tie; "
            "both options technically viable but have different long-term cost profiles"
        ),
        "escalation_type": "Decision",
        "specific_ask":    (
            "Need architecture review meeting scheduled within two weeks "
            "to unblock engineering work currently on hold pending this decision"
        ),
        "resolved":           False,
        "resolved_at":        None,
        "resolution_description": None,
    },
]


def run_seed():
    """Run the full seed silently and return insertion counts.

    Wipes all tables, re-seeds default metrics, then inserts all mock data.
    Returns dict with keys: engineers, signals, annotations, blockers.
    """
    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    for table in (
        "signals",
        "metric_annotations",
        "strategic_context_history",
        "manager_blockers",
        "briefs",
        "retrospectives",
        "app_state",
        "engineers",
        "metrics",
    ):
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()

    from database import seed_default_metrics
    seed_default_metrics()

    cursor.execute("SELECT id, name FROM metrics WHERE is_default = 1")
    metrics = {row["name"]: row["id"] for row in cursor.fetchall()}

    # Engineers
    engineer_ids = {}
    for name, role in ENGINEERS:
        cursor.execute("INSERT INTO engineers (name, role) VALUES (?, ?)", (name, role))
        engineer_ids[name] = cursor.lastrowid
    conn.commit()

    # Signals
    signal_count = 0
    for name, weekly_signals in SIGNAL_DATA.items():
        eid = engineer_ids[name]
        for week_idx, sig in enumerate(weekly_signals):
            logged_at = SIGNAL_WEEKS[week_idx].isoformat() + " 09:00:00"
            cursor.execute(
                """
                INSERT INTO signals
                    (engineer_id, energy_level, delivery_signal, growth_signal,
                     stress_level, stress_source, uncertainty_level, uncertainty_source,
                     observation, logged_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    eid,
                    sig["energy_level"], sig["delivery_signal"], sig["growth_signal"],
                    sig["stress_level"], sig["stress_source"],
                    sig["uncertainty_level"], sig["uncertainty_source"],
                    sig["observation"], logged_at,
                ),
            )
            signal_count += 1
    conn.commit()

    # Metric annotations
    annotation_count = 0
    for metric_name, annotations in ANNOTATION_DATA.items():
        mid = metrics.get(metric_name)
        if mid is None:
            continue
        for week_idx, (value, classification, explanation) in enumerate(annotations):
            annotated_at = SIGNAL_WEEKS[week_idx].isoformat() + " 10:00:00"
            cursor.execute(
                """
                INSERT INTO metric_annotations
                    (metric_id, current_value, classification, explanation, annotated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (mid, value, classification, explanation, annotated_at),
            )
            annotation_count += 1
    conn.commit()

    # Strategic context
    for metric_name, ctx in STRATEGIC_CONTEXTS.items():
        mid = metrics.get(metric_name)
        if mid:
            cursor.execute(
                """
                UPDATE metrics
                SET strategic_context = ?, strategic_context_updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (ctx, mid),
            )
    conn.commit()

    # Manager blockers
    blocker_count = 0
    for b in BLOCKERS:
        cursor.execute(
            """
            INSERT INTO manager_blockers
                (description, open_since, what_tried, options_remaining,
                 escalation_type, specific_ask, resolved, resolved_at, resolution_description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                b["description"], b["open_since"],
                b["what_tried"], b["options_remaining"],
                b["escalation_type"], b["specific_ask"],
                1 if b["resolved"] else 0,
                b["resolved_at"], b["resolution_description"],
            ),
        )
        blocker_count += 1
    conn.commit()

    conn.close()

    return {
        "engineers":   len(ENGINEERS),
        "signals":     signal_count,
        "annotations": annotation_count,
        "blockers":    blocker_count,
    }


def seed():
    print("=" * 55)
    print("  Team Signal Translator — Mock Data Seeder")
    print("=" * 55)

    counts = run_seed()

    print("\n" + "=" * 55)
    print("  Seeding complete!")
    print("=" * 55)
    print(f"  Engineers           {counts['engineers']:>4}")
    print(f"  Signals             {counts['signals']:>4}   ({counts['engineers']} engineers × 8 weeks)")
    print(f"  Metric annotations  {counts['annotations']:>4}   (4 metrics × 8 weeks)")
    print(f"  Manager blockers    {counts['blockers']:>4}")
    print("=" * 55)
    print(f"\nDate range covered:")
    print(f"  Oldest signal:  {SIGNAL_WEEKS[0].isoformat()}")
    print(f"  Newest signal:  {SIGNAL_WEEKS[-1].isoformat()}")
    print(f"  Reference date: {TODAY.isoformat()}")


if __name__ == "__main__":
    seed()

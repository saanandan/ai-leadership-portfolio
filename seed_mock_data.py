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

# ── Reference date & 13-week range ───────────────────────────────────────────
TODAY      = date(2026, 5, 31)
START_DATE = date(2026, 3, 1)
SIGNAL_WEEKS = [START_DATE + timedelta(weeks=w) for w in range(13)]
# Week indices (0-based):
#  0 = Mar  1   1 = Mar  8   2 = Mar 15   3 = Mar 22   4 = Mar 29
#  5 = Apr  5   6 = Apr 12   7 = Apr 19   8 = Apr 26   9 = May  3
# 10 = May 10  11 = May 17  12 = May 24

# ── Engineers ─────────────────────────────────────────────────────────────────
ENGINEERS = [
    ("Sarah Chen",     "Senior Engineer"),
    ("Amy Rodriguez",  "Engineer III"),
    ("Priya Patel",    "Engineer II"),
    ("Omar Hassan",    "Senior Engineer"),
    ("Lisa Thompson",  "Engineer II"),
    ("James Kim",      "Staff Engineer"),
    ("Marcus Johnson", "Staff Engineer"),
    ("Derek Williams", "Senior Engineer"),
]

# ── Signal helper ─────────────────────────────────────────────────────────────
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

# ── Signal data (13 entries per engineer, oldest → newest) ───────────────────
SIGNAL_DATA = {

    # ── Sarah Chen — consistent bright spot all quarter ───────────────────────
    "Sarah Chen": [
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Excellent start to the quarter. Shipped API integration ahead of schedule."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Strong PR throughput. Proactively unblocking teammates on auth migration."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Led architecture review for new payment service. Sharp and well-prepared."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Solid delivery. Raised test coverage gap proactively before it became an issue."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Shipped test automation framework. Coverage improving across the team."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Stepped up to own CICD coverage remediation without being asked. Strong ownership."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Leading coverage push. Executing well under extra load. No signs of strain."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Coverage work on track. Delivered two sprint tickets simultaneously."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Coverage target in sight. Highest-impact engineer on the team this sprint."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Coverage approaching target. Positive energy throughout a demanding sprint."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Coverage target achieved. Team celebrated. Excellent end to a long remediation push."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Back to feature delivery post-remediation. Thriving. No lingering effects from heavy Q1 load."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Outstanding quarter close. Consistent excellence from week one to week thirteen."),
    ],

    # ── Amy Rodriguez — solid and reliable throughout ─────────────────────────
    "Amy Rodriguez": [
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Good start. Reliable delivery and positive team presence."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Strong sprint. Completed feature ahead of plan. High quality output."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Consistent contributor. Raising the bar in code reviews."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "High quality output. Good pairing with junior engineers."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Dependable delivery. Uplifting team standards in code review and design."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Solid delivery despite CICD disruption this sprint. Stayed focused."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Strong week. Delivered key feature on time. Good energy in standups."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Reliable output. Good sprint velocity maintained."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Shipped important integration. Clean execution from design through deployment."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Consistent quality. Positive team collaborator every week."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "High energy. Delivered two features this sprint. Good momentum into Q3."),
        s(4, "On Track", "Growing", "Low", None, "Low", None, "Solid week. Good delivery and positive attitude throughout."),
        s(5, "On Track", "Growing", "Low", None, "Low", None, "Strong quarter close. Reliable and high quality every single sprint."),
    ],

    # ── Priya Patel — growing, workload stress from week 6 onward ─────────────
    "Priya Patel": [
        s(3, "On Track", "Growing", "Low",      None,       "Low", None, "Ramping up well. Asking good questions in code review."),
        s(3, "On Track", "Growing", "Low",      None,       "Low", None, "Steady progress. Completed first solo feature."),
        s(3, "On Track", "Growing", "Low",      None,       "Low", None, "Good output. Growing confidence in the codebase. Pairing sessions going well."),
        s(3, "On Track", "Growing", "Low",      None,       "Low", None, "Consistent delivery. Strong pairing sessions with Sarah on testing."),
        s(3, "On Track", "Growing", "Low",      None,       "Low", None, "Sprint commitment met. Growth trajectory clearly positive."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Workload increased with CICD coverage remediation. Managing but feels stretched."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Owning vuln remediation work alongside normal sprint load. Flagged feeling stretched."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Sprint commitments met but working longer hours. Workload is the primary stressor."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Steady output despite heavy load. Mentioned feeling overwhelmed at sprint end."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Delivered on commitments. Workload pressure continuing but she is managing it."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Consistent output. Workload improving as remediation work clears."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Good sprint. Workload more manageable as vuln work winds down."),
        s(3, "On Track", "Growing", "Moderate", "Workload", "Low", None, "Solid delivery. Growth is clear — handling significantly more than week one."),
    ],

    # ── Omar Hassan — reliable, coasting, no flags all quarter ───────────────
    "Omar Hassan": [
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Reliable delivery. Consistent pace on assigned work."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Good sprint. Solid and dependable as always."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Steady progress. Team relies on his stability and predictability."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Consistent contributor. Unblocked two teammates without being asked."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "On track. No concerns flagged. Predictable delivery."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Dependable week. Solid presence in ceremonies and reviews."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Consistent pace. Good team presence. Reliable anchor for the team."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Reliable output. Calm focus during a noisy sprint."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Steady delivery. Stable energy throughout the sprint."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Good sprint. Consistent and dependable contribution."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "On track. No concerns. Delivered every commitment."),
        s(4, "On Track", "Coasting", "Low", None, "Low", None, "Solid week. Stable as always."),
        s(3, "On Track", "Coasting", "Low", None, "Low", None, "Consistent close to Q2. Reliable anchor for the team all quarter."),
    ],

    # ── Lisa Thompson — growing, uncertainty about team direction from week 7 ─
    "Lisa Thompson": [
        s(3, "On Track", "Growing", "Low", None, "Low",      None,            "Ramping up well. Engaged and curious about the codebase."),
        s(3, "On Track", "Growing", "Low", None, "Low",      None,            "Steady progress. Asking good questions in 1:1 and standups."),
        s(3, "On Track", "Growing", "Low", None, "Low",      None,            "Consistent delivery. Learning the codebase quickly."),
        s(3, "On Track", "Growing", "Low", None, "Low",      None,            "Sprint commitment met. Growing confidence in taking on harder tickets."),
        s(4, "On Track", "Growing", "Low", None, "Low",      None,            "Energy up this week. Good delivery and positive attitude."),
        s(2, "On Track", "Growing", "Low", None, "Low",      None,            "Lower energy this week. Mentioned personal factors. Delivered all commitments."),
        s(3, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Stable output. Started asking questions about team direction and roadmap in 1:1."),
        s(4, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Good sprint. Uncertainty about team direction persists but not blocking delivery."),
        s(2, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Energy dip. Delivered but flagged uncertainty about where the team is heading in the org."),
        s(4, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Bounced back well. Good week. Uncertainty about direction still present in 1:1."),
        s(3, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Consistent delivery. Team direction uncertainty ongoing — worth addressing in all-hands."),
        s(2, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Energy lower again. Delivering but team direction questions increasing in frequency."),
        s(3, "On Track", "Growing", "Low", None, "Moderate", "Team direction", "Stable close to Q2. Team direction uncertainty is a persistent theme worth resolving."),
    ],

    # ── James Kim — coasting, declining energy, at risk weeks 11-13 ──────────
    "James Kim": [
        s(3, "On Track", "Growing",  "Low",      None,                  "Low",  None,                "Delivering on scope. Engaged in planning discussions."),
        s(3, "On Track", "Growing",  "Low",      None,                  "Low",  None,                "Good output. Thoughtful contributor in design reviews."),
        s(3, "On Track", "Growing",  "Low",      None,                  "Low",  None,                "Consistent delivery. Good team collaborator."),
        s(3, "On Track", "Growing",  "Low",      None,                  "Low",  None,                "Sprint commitment met. Solid week."),
        s(3, "On Track", "Coasting", "Low",      None,                  "Low",  None,                "Delivering but not stretching beyond assigned scope. Engagement slightly reduced."),
        s(3, "On Track", "Coasting", "Low",      None,                  "Low",  None,                "Consistent output. Less invested in roadmap discussions this sprint."),
        s(3, "On Track", "Coasting", "Low",      None,                  "Low",  None,                "On time delivery. No growth signals observed. Worth a check-in on motivation."),
        s(3, "On Track", "Coasting", "Moderate", "Shifting priorities", "Low",  None,                "Mentioned frustration with shifting priorities mid-sprint. Delivered but energy is flat."),
        s(2, "On Track", "Coasting", "Moderate", "Shifting priorities", "Low",  None,                "Energy dropped noticeably. Still delivering but visibly disengaged."),
        s(2, "On Track", "Coasting", "Moderate", "Shifting priorities", "Low",  None,                "Still on track but energy remains low. Mentioned confusion about strategic direction."),
        s(2, "At Risk",  "Coasting", "Moderate", "Shifting priorities", "High", "Company direction", "At risk. Slipping on commitments. Cited company direction uncertainty as primary concern."),
        s(2, "At Risk",  "Coasting", "Moderate", "Shifting priorities", "High", "Company direction", "Continuing at risk. Said he does not know what the company is optimizing for. Needs clarity."),
        s(2, "At Risk",  "Coasting", "Moderate", "Shifting priorities", "High", "Company direction", "Still at risk. Uncertainty about company direction affecting output. Needs urgent roadmap clarity."),
    ],

    # ── Marcus Johnson — burnout arc, retention risk by week 12 ──────────────
    "Marcus Johnson": [
        # Weeks 1-3: high performer, everything fine
        s(5, "On Track", "Growing",    "Low",      None,                      "Low",  None,                     "Strong start to the quarter. Leading auth module architecture. High initiative."),
        s(5, "On Track", "Growing",    "Low",      None,                      "Low",  None,                     "Excellent delivery. Proactively unblocking teammates. Positive energy."),
        s(5, "On Track", "Growing",    "Low",      None,                      "Low",  None,                     "Shipped key feature two days ahead of plan. Positive force on team culture."),
        # Weeks 4-5: first signs of pressure
        s(4, "On Track", "Growing",    "Moderate", "Organizational pressure", "Low",  None,                     "Good delivery. Mentioned organizational changes creating some background pressure."),
        s(4, "On Track", "Growing",    "Moderate", "Organizational pressure", "Low",  None,                     "Sprint commitment met. Organizational pressure noted again. Worth monitoring."),
        # Weeks 6-7: delivery starting to slip
        s(4, "At Risk",  "Coasting",   "Moderate", "Organizational pressure", "Moderate", "Shifting priorities", "Deliverable slipped slightly. Mentioned feeling pulled between competing priorities."),
        s(4, "At Risk",  "Coasting",   "Moderate", "Organizational pressure", "Moderate", "Shifting priorities", "At risk on sprint goal. Organizational uncertainty affecting focus and follow-through."),
        # Weeks 8-9: stress visibly elevated
        s(3, "At Risk",  "Coasting",   "High",     "Organizational pressure", "High", "Shifting priorities",    "Stress visibly elevated. Deliverable missed for second week. Mentioned feeling overwhelmed."),
        s(3, "At Risk",  "Coasting",   "High",     "Organizational pressure", "High", "Shifting priorities",    "Engineer mentioned feeling overwhelmed in 1:1. Suggested taking time off."),
        # Weeks 10-11: struggling, retention signals
        s(3, "At Risk",  "Struggling", "High",     "Organizational pressure", "High", "Company direction",      "Struggling to maintain pace. Mentioned considering other opportunities in 1:1."),
        s(3, "At Risk",  "Struggling", "High",     "Organizational pressure", "High", "Company direction",      "At risk continues. Said he does not see a path forward. Skip-level awareness needed."),
        # Week 12: explicit retention risk
        s(2, "Blocked",  "Struggling", "High",     "Organizational pressure", "High", "Company direction",      "Engineer asked about leave options. Flagged to director. Retention risk."),
        # Week 13: no improvement
        s(2, "Blocked",  "Struggling", "High",     "Organizational pressure", "High", "Company direction",      "Still at retention risk. No improvement. Immediate intervention needed."),
    ],

    # ── Derek Williams — external blocker story, blocked weeks 11-13 ─────────
    "Derek Williams": [
        # Weeks 1-9: fine, building toward SSO integration
        s(4, "On Track", "Coasting",   "Low",      None,             "Low", None, "Solid week. Good delivery on assigned tasks."),
        s(3, "On Track", "Coasting",   "Low",      None,             "Low", None, "Consistent output. Steady pace."),
        s(4, "On Track", "Coasting",   "Low",      None,             "Low", None, "Good sprint. Delivered on commitment."),
        s(3, "On Track", "Coasting",   "Low",      None,             "Low", None, "Steady delivery. Started SSO integration work. Scoping the requirements."),
        s(4, "On Track", "Coasting",   "Low",      None,             "Low", None, "Making progress on SSO integration. Identifying dependency on cyber team."),
        s(3, "On Track", "Coasting",   "Low",      None,             "Low", None, "Good sprint. SSO integration progressing. Request to cyber team submitted."),
        s(4, "On Track", "Coasting",   "Low",      None,             "Low", None, "Consistent delivery. SSO work requires cyber team redirect URL — first follow-up sent."),
        s(3, "On Track", "Coasting",   "Low",      None,             "Low", None, "Awaiting cyber team response on SSO redirect URL. Continuing other work in the meantime."),
        s(3, "On Track", "Coasting",   "Low",      None,             "Low", None, "Still awaiting cyber team. Second outreach sent. No response yet. Starting to track."),
        # Week 10: blocker emerging
        s(3, "At Risk",  "Coasting",   "Moderate", "Team dynamics",  "Low", None, "Third outreach to cyber team with no response. SSO work at risk. Formal escalation request submitted."),
        # Weeks 11-13: fully blocked
        s(2, "Blocked",  "Struggling", "High",     "Team dynamics",  "Low", None, "Blocked on SSO redirect URL dependency with cyber team. Three outreach attempts with no response. Cannot progress without escalation."),
        s(2, "Blocked",  "Struggling", "High",     "Team dynamics",  "Low", None, "Blocked on SSO redirect URL dependency with cyber team. Three outreach attempts with no response. Cannot progress without escalation."),
        s(2, "Blocked",  "Struggling", "High",     "Team dynamics",  "Low", None, "Blocked on SSO redirect URL dependency with cyber team. Three outreach attempts with no response. Cannot progress without escalation."),
    ],
}

# ── Metric annotations ────────────────────────────────────────────────────────
# {metric_name: {target_value, strategic_context, weeks: [(value, classification, explanation, owner_name_or_None)]}}
# weeks are oldest → newest, aligned to SIGNAL_WEEKS (13 entries each)
ANNOTATION_DATA = {

    "CICD Health": {
        "target_value": "80% code coverage",
        "strategic_context": (
            "Pipeline team manages shared infrastructure. "
            "Reliability affects all teams."
        ),
        "weeks": [
            # Weeks 1-6: healthy
            ("88%", "Amber",  "CICD pipeline healthy. Coverage above target.", None),
            ("88%", "Amber",  "CICD pipeline healthy. Coverage above target.", None),
            ("88%", "Amber",  "CICD pipeline healthy. Coverage above target.", None),
            ("88%", "Amber",  "CICD pipeline healthy. Coverage above target.", None),
            ("88%", "Amber",  "CICD pipeline healthy. Coverage above target.", None),
            ("88%", "Amber",  "CICD pipeline healthy. Coverage above target.", None),
            # Week 7: retroactive rule hits
            ("65%", "Red",    "New org-wide CICD rule requiring 80% code coverage introduced mid-sprint. Applied retroactively to legacy code. Team scrambling to remediate while continuing feature delivery.", "Sarah Chen"),
            # Weeks 8-9: remediation in progress
            ("70%", "Red",    "Team actively remediating legacy code coverage. On track to recover by week 11.", "Sarah Chen"),
            ("70%", "Red",    "Coverage remediation continuing. Legacy modules being addressed one by one. Trajectory positive.", "Sarah Chen"),
            # Weeks 10-11: improving
            ("76%", "Orange", "Coverage improving steadily. Two legacy modules remaining.", None),
            ("76%", "Orange", "Final two legacy modules in remediation. Target expected next sprint.", None),
            # Weeks 12-13: recovered
            ("85%", "Amber",  "Target achieved and exceeded. Coverage stable at 85%.", None),
            ("85%", "Amber",  "Coverage holding at 85%. Remediation complete. No regression introduced.", None),
        ],
    },

    "Vuln Remediation": {
        "target_value": "0 past-due vulns",
        "strategic_context": (
            "All 40 vulns are non-exploitable and formally dispositioned. "
            "Compliance team acceptance is the only remaining step. "
            "System decommissions end of June — investment in remediation not justified."
        ),
        "weeks": [
            # Weeks 1-3: existing backlog being cleared
            ("12 open vulns", "Orange", "12 vulns past due. Team remediating actively. On track to clear by end of March.", None),
            ("10 open vulns", "Orange", "Good progress. Down to 10. Steady remediation pace.", None),
            ("6 open vulns",  "Orange", "Continued progress. 6 remaining, all being actively worked.", None),
            # Weeks 4-5: nearly clear
            ("5 open vulns",  "Orange", "Good progress. 5 remaining, all being actively worked.", None),
            ("2 open vulns",  "Orange", "Almost clear. 2 remaining, both scheduled for this sprint.", None),
            # Week 6: new batch from automated scan
            ("40 open vulns", "Red",    "New batch of vulns flagged by automated scan. All reviewed and dispositioned as non-exploitable. Pending acceptance from volunteer-led compliance team.", "Priya Patel"),
            # Weeks 7-13: stuck waiting on compliance team — all non-exploitable
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "All 40 vulns dispositioned as non-exploitable. Compliance team review in progress. No security exposure.", None),
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "No change. All 40 non-exploitable. Awaiting compliance team sign-off. System decommissions end of June.", None),
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "40 vulns, all non-exploitable. Compliance team the only remaining gate. No security risk present.", None),
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "Still waiting on compliance team. All 40 vulns non-exploitable. Priority not justified given June decommission.", None),
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "Compliance review ongoing. All 40 non-exploitable and formally documented. System retires June 30.", None),
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "40 vulns unchanged. All non-exploitable. Compliance team engaged but slow to formalize acceptance.", None),
            ("40 open vulns — all dispositioned non-exploitable", "Orange", "All 40 vulns non-exploitable. Compliance team acceptance pending. On track for system decommission end of June.", None),
        ],
    },

    "Deployment Success Rate": {
        "target_value": "95%",
        "strategic_context": (
            "Two systemic constraints: PO sign-off adds cycle time, upstream partner QA data unreliable. "
            "Pipeline team infrastructure failures also periodically impact this metric."
        ),
        "weeks": [
            # Weeks 1-5: stable but below target due to PO sign-off cycle
            ("94%", "Orange", "Slightly below 95% target. Release process requires PO sign-off adding cycle time.", None),
            ("94%", "Orange", "Slightly below 95% target. Release process requires PO sign-off adding cycle time.", None),
            ("94%", "Orange", "Stable at 94%. PO sign-off process unchanged. Targeting process improvement in Q3.", None),
            ("94%", "Orange", "Holding at 94%. No new issues. PO testing cycle remains the constraint.", None),
            ("94%", "Orange", "94% — consistent. Upstream QA data reliability also adding occasional friction.", None),
            # Week 6: pipeline team incident
            ("78%", "Red",    "Rate dropped due to pipeline team pushing an undocumented change to build configuration, causing 4 deployment failures. Our deployments were 100% successful once the pipeline was stable. Pipeline-caused failures should be excluded from team metrics.", "Derek Williams"),
            # Week 7: recovered
            ("92%", "Orange", "Recovered after pipeline stabilized. Failure window caused entirely by undocumented pipeline team change. Post-mortem completed.", None),
            # Weeks 8-13: stable, systemic constraints ongoing
            ("93%", "Orange", "Stable at 93%. Main constraint is PO testing cycle and upstream QA data reliability.", None),
            ("93%", "Orange", "Stable at 93%. No incidents this sprint. PO sign-off cycle improvement scoped for Q3.", None),
            ("93%", "Orange", "Holding at 93%. Upstream QA data quality improved slightly this week.", None),
            ("93%", "Orange", "93% consistent. Q3 process improvement work to address PO sign-off cycle is planned.", None),
            ("93%", "Orange", "93% stable. No incidents. Systemic constraints documented and improvement plan in progress.", None),
            ("93%", "Orange", "Strong close to Q2 at 93%. Systemic improvement plan agreed with PO for Q3.", None),
        ],
    },

    "Test Coverage": {
        "target_value": "80%",
        "strategic_context": (
            "New greenfield team formed February 2026. "
            "Coverage will improve as codebase matures and requirements stabilize."
        ),
        "weeks": [
            # Weeks 1-4: greenfield baseline
            ("45%", "Red",    "Greenfield team building from scratch since February. New team, large PRs, requirements evolving rapidly.", None),
            ("46%", "Red",    "Incremental improvement. Team establishing testing patterns as requirements stabilize.", None),
            ("48%", "Red",    "Coverage improving each sprint. Foundation being built deliberately.", None),
            ("50%", "Red",    "Steady improvement. Team adopting TDD practices for new feature work.", None),
            # Weeks 5-7: improving with Sarah leading
            ("58%", "Red",    "Coverage improving each sprint. Team establishing testing standards.", "Sarah Chen"),
            ("60%", "Red",    "Meaningful progress. Testing patterns now consistent across the team.", "Sarah Chen"),
            ("63%", "Red",    "Coverage improving steadily. Below target but trajectory is clear.", "Sarah Chen"),
            # Weeks 8-10: above Red threshold
            ("68%", "Orange", "Good progress. Team has established testing standards. Target within reach.", None),
            ("70%", "Orange", "Coverage at 70%. Steady improvement sprint-over-sprint.", None),
            ("72%", "Orange", "Continuing to improve. Two more legacy modules to cover.", None),
            # Weeks 11-13: approaching target
            ("74%", "Orange", "On track to hit 80% target by end of Q3.", "Sarah Chen"),
            ("76%", "Orange", "Coverage improving. Target ahead of schedule.", "Sarah Chen"),
            ("78%", "Orange", "78% — highest this quarter. On track to hit 80% target by end of Q3.", "Sarah Chen"),
        ],
    },

    "Production Incidents": {
        "target_value": "0 P1 incidents, fewer than 3 P2 per quarter",
        "strategic_context": (
            "Recurring P2 incidents caused by entitlements API owned by a separate org. "
            "Our team responds within SLA every time. "
            "2 incidents in Q2 so far — pattern warrants formal escalation."
        ),
        "weeks": [
            # Weeks 1-3: clean
            ("0 incidents", "Amber",  "Clean period. No incidents.", None),
            ("0 incidents", "Amber",  "No incidents. All services healthy.", None),
            ("0 incidents", "Amber",  "No incidents. On-call rotation smooth.", None),
            # Week 4: first P2
            ("1 P2 incident", "Orange",
             "1 P2 (High) · Owned by: Dependency failure · Owning team: Entitlements API team · Status: Resolved\n\n"
             "Entitlements API caused 47 minutes of application inaccessibility. Our team responded within SLA. "
             "Root cause owned by entitlements API team. Post-mortem completed.", None),
            # Weeks 5-8: clean, monitoring
            ("0 incidents", "Amber",  "No incidents. Post-mortem action items from week-4 P2 completed.", None),
            ("0 incidents", "Amber",  "No incidents. Monitoring entitlements API for recurrence.", None),
            ("0 incidents", "Amber",  "No incidents. Systems stable.", None),
            ("0 incidents", "Amber",  "Clean week. No production incidents.", None),
            # Week 9: second P2 — pattern emerging
            ("1 P2 incident", "Orange",
             "1 P2 (High) · Owned by: Dependency failure · Owning team: Entitlements API team · Status: Resolved\n\n"
             "Second entitlements API incident this quarter. 2 hours of downtime. Our team responded within SLA. "
             "Pattern is now clear — formal escalation to entitlements API team leadership recommended.", None),
            # Weeks 10-13: clean, escalation pending
            ("0 incidents", "Amber",  "No incidents. Entitlements API team notified of recurring pattern.", None),
            ("0 incidents", "Amber",  "No incidents. Monitoring continues.", None),
            ("0 incidents", "Amber",  "No incidents. Quiet period.", None),
            ("0 incidents", "Amber",  "No incidents. Q2 total: 2 P2 incidents — within threshold but pattern warrants action.", None),
        ],
    },
}

# ── Manager blockers ──────────────────────────────────────────────────────────
BLOCKERS = [
    {
        # Resolved after director escalation — the SSO story
        "description": "SSO redirect URL update required for new authentication flow",
        "open_since":  date(2026, 3, 15).isoformat(),
        "what_tried":  (
            "Emailed cyber team 4 times. "
            "Attended their weekly sync twice. "
            "Escalated to their manager once. "
            "Submitted formal request through ticketing system."
        ),
        "options_remaining": (
            "No further options within my control. "
            "Cyber team has no published SLA."
        ),
        "escalation_type": "Nudge someone who is not responding to me",
        "specific_ask":    (
            "Need director to escalate directly to cyber team VP. "
            "8 weeks of outreach has produced no response. "
            "Derek Williams is fully blocked and sprint velocity is impacted."
        ),
        "resolved":               True,
        "resolved_at":            date(2026, 5, 10).isoformat(),
        "resolution_description": (
            "Director escalated to cyber team VP. "
            "Redirect URL updated within 48 hours of escalation. "
            "8 weeks of waiting resolved in 2 days with the right level of intervention."
        ),
    },
    {
        # Aging open — headcount
        "description": "Headcount approval pending for senior engineer backfill — role open since last quarter",
        "open_since":  date(2026, 4, 19).isoformat(),
        "what_tried":  (
            "Submitted headcount request with full business justification. "
            "Followed up with HR twice. "
            "Escalated to director once."
        ),
        "options_remaining": (
            "Cannot proceed without approval. "
            "Team is under capacity and this is the primary constraint on greenfield delivery."
        ),
        "escalation_type": "Approval to proceed with my proposed solution",
        "specific_ask":    (
            "Approve headcount request so recruiting can begin. "
            "Capacity deficit is the primary constraint on greenfield delivery timeline."
        ),
        "resolved":               False,
        "resolved_at":            None,
        "resolution_description": None,
    },
    {
        # Recent open — architecture decision
        "description": "Architecture decision required: monolith-first vs microservices for new authentication module",
        "open_since":  date(2026, 5, 17).isoformat(),
        "what_tried":  (
            "Documented both approaches with full tradeoff analysis. "
            "Shared with team leads. "
            "Received conflicting opinions with no consensus."
        ),
        "options_remaining": (
            "Cannot begin development until direction is confirmed. "
            "Three engineers are waiting on this decision."
        ),
        "escalation_type": "Choose between two equally good options",
        "specific_ask":    (
            "Review tradeoff document and make the call. "
            "Monolith-first is faster to deliver. "
            "Microservices is cleaner long term. "
            "Either is fine — we need a decision to unblock the team."
        ),
        "resolved":               False,
        "resolved_at":            None,
        "resolution_description": None,
    },
]


def run_seed():
    """Wipe all data, re-seed default metrics, insert 13 weeks of mock data.

    Returns dict with counts: engineers, signals, annotations, blockers.
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
                    sig["stress_level"],  sig["stress_source"],
                    sig["uncertainty_level"], sig["uncertainty_source"],
                    sig["observation"], logged_at,
                ),
            )
            signal_count += 1
    conn.commit()

    # Metric annotations + strategic context
    annotation_count = 0
    for metric_name, data in ANNOTATION_DATA.items():
        mid = metrics.get(metric_name)
        if mid is None:
            continue

        cursor.execute(
            """
            UPDATE metrics
            SET strategic_context = ?, strategic_context_updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (data["strategic_context"], mid),
        )

        for week_idx, (value, classification, explanation, owner_name) in enumerate(data["weeks"]):
            annotated_at = SIGNAL_WEEKS[week_idx].isoformat() + " 10:00:00"
            owner_id = engineer_ids.get(owner_name) if owner_name else None
            cursor.execute(
                """
                INSERT INTO metric_annotations
                    (metric_id, current_value, target_value, classification, explanation,
                     remediation_owner_id, annotated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (mid, value, data["target_value"], classification, explanation, owner_id, annotated_at),
            )
            annotation_count += 1
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
    print("=" * 65)
    print("  Team Signal Translator — Mock Data Seeder")
    print("=" * 65)

    counts = run_seed()

    conn = get_connection()
    cursor = conn.cursor()

    # Per-engineer breakdown
    print(f"\n{'─' * 65}")
    print("  ENGINEERS & SIGNALS")
    print(f"{'─' * 65}")
    cursor.execute("""
        SELECT e.name, e.role, COUNT(s.id) AS n,
               MIN(DATE(s.logged_at)) AS first_signal,
               MAX(DATE(s.logged_at)) AS last_signal
        FROM engineers e
        LEFT JOIN signals s ON s.engineer_id = e.id
        GROUP BY e.id
        ORDER BY e.name
    """)
    for row in cursor.fetchall():
        print(
            f"  {row['name']:<22} {row['role']:<18}"
            f"  {row['n']:>2} signals  "
            f"({row['first_signal']} → {row['last_signal']})"
        )

    # Per-metric breakdown
    print(f"\n{'─' * 65}")
    print("  METRICS & ANNOTATIONS")
    print(f"{'─' * 65}")
    cursor.execute("""
        SELECT m.name,
               COUNT(ma.id)                          AS n,
               MIN(DATE(ma.annotated_at))            AS first_ann,
               MAX(DATE(ma.annotated_at))            AS last_ann,
               m.strategic_context IS NOT NULL       AS has_ctx,
               MAX(ma.target_value)                  AS target
        FROM metrics m
        LEFT JOIN metric_annotations ma ON ma.metric_id = m.id
        WHERE m.is_default = 1
        GROUP BY m.id
        ORDER BY m.name
    """)
    for row in cursor.fetchall():
        ctx = "✓ context" if row["has_ctx"] else "no context"
        print(
            f"  {row['name']:<28}  {row['n']:>2} annotations  "
            f"({row['first_ann']} → {row['last_ann']})  "
            f"{ctx}  target: {row['target']}"
        )

    # Blocker breakdown
    print(f"\n{'─' * 65}")
    print("  MANAGER BLOCKERS")
    print(f"{'─' * 65}")
    cursor.execute(
        "SELECT description, open_since, resolved, resolved_at FROM manager_blockers ORDER BY open_since"
    )
    for row in cursor.fetchall():
        if row["resolved"]:
            status = f"✅ Resolved {row['resolved_at'][:10]}"
        else:
            status = "🔴 Open"
        desc = row["description"][:50] + ("..." if len(row["description"]) > 50 else "")
        print(f"  {status:<26}  since {row['open_since']}  {desc}")

    conn.close()

    # Totals
    print(f"\n{'─' * 65}")
    print("  TOTALS")
    print(f"{'─' * 65}")
    print(f"  Engineers    {counts['engineers']:>3}")
    print(f"  Signals      {counts['signals']:>3}   ({counts['engineers']} engineers × 13 weeks)")
    print(f"  Annotations  {counts['annotations']:>3}   (5 metrics × 13 weeks)")
    print(f"  Blockers     {counts['blockers']:>3}   (1 resolved, 2 active)")
    print(f"\n  Date range:  {SIGNAL_WEEKS[0].isoformat()}  →  {SIGNAL_WEEKS[-1].isoformat()}")
    print(f"  Reference:   {TODAY.isoformat()}")
    print("=" * 65)


if __name__ == "__main__":
    seed()

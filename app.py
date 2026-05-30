import streamlit as st
import pandas as pd
from datetime import datetime
from database import (
    get_connection, get_all_engineers, initialize_database,
    get_latest_signal_per_engineer, get_latest_annotation_per_metric,
    get_aging_blockers, get_active_trend_flags, get_metric_trend_flags,
    detect_team_wide_patterns, get_all_metrics,
)
from dotenv import load_dotenv
from components.navigation import show_navigation
import os

# Load environment variables
load_dotenv()

def check_onboarding_complete():
    """Check if onboarding has been completed"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM app_state WHERE key = 'onboarding_complete'")
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None and result['value'] == 'true'
        
    except Exception as e:
        # If table doesn't exist or other error, assume onboarding not complete
        return False

def set_onboarding_complete():
    """Set onboarding as completed"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO app_state (key, value) VALUES ('onboarding_complete', 'true')
        """)
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        st.error(f"Failed to save onboarding status: {e}")
        return False

def show_onboarding():
    """Display the onboarding screen"""
    st.set_page_config(
        page_title="Engineering Leadership Signal Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("# 📊 Engineering Leadership Signal Tool")
    st.markdown("---")

    st.markdown("### People leadership still matters.")
    st.markdown(
        "AI is changing how fast we build. It is not changing the fact that humans build it. "
        "The signals that predict team health — energy, stress, uncertainty, growth — live in 1:1 conversations, "
        "not dashboards. This tool captures them consistently so nothing gets lost."
    )

    st.markdown("### Context is what makes data useful.")
    st.markdown(
        "A metric without context is just a number. 60% vuln remediation looks alarming. "
        "It looks different when you know the system is being retired next quarter. "
        "This tool lets you attach the human context to every metric at the point of observation "
        "— so leadership sees the story, not just the number."
    )

    st.markdown("### If everything is equally important, nothing is.")
    st.markdown(
        "This tool automatically detects patterns that matter — sustained stress, aging blockers, "
        "metrics that have been red for the same reason three times in a row. "
        "It surfaces what needs attention so you can focus your energy on the right things."
    )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", width='stretch', type="primary"):
            if set_onboarding_complete():
                st.success("Welcome! Setting up your team...")
                st.rerun()
            else:
                st.error("Failed to save your progress. Please try again.")

def show_main_app():
    """Display the main application after onboarding"""
    st.set_page_config(
        page_title="Engineering Leadership Signal Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
<style>
.dataframe {font-size: 14px !important;}
.dataframe td {padding: 8px !important;}
.dataframe th {padding: 8px !important; font-size: 13px !important;}
</style>
""", unsafe_allow_html=True)

    # Sidebar navigation
    show_navigation()

    with st.sidebar:
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        if st.button("🔄 Reset Onboarding", width='stretch', help="For testing only"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM app_state WHERE key = 'onboarding_complete'")
            conn.commit()
            conn.close()
            st.rerun()
    
    # Main content
    engineers = get_all_engineers()
    
    if engineers:
        st.markdown("# 📊 Engineering Leadership Signal Tool")
        st.markdown("---")

        # ── Fetch all dashboard data ────────────────────────────────────────
        latest_signals = get_latest_signal_per_engineer()
        signal_by_engineer = {s['engineer_id']: s for s in latest_signals}

        trend_flags = get_active_trend_flags()
        flags_by_engineer = {}
        for flag in trend_flags:
            flags_by_engineer.setdefault(flag['engineer_id'], []).append(flag['flag_type'])

        patterns = detect_team_wide_patterns()
        aging_blockers_list = get_aging_blockers()
        latest_annotations = get_latest_annotation_per_metric()
        ann_by_metric = {a['metric_id']: a for a in latest_annotations}
        all_metrics = get_all_metrics()
        metric_flags = get_metric_trend_flags()

        # ── Alert Banners ───────────────────────────────────────────────────
        for pattern in patterns:
            label = "Team-Wide Stress Alert" if pattern['pattern_type'] == 'stress_pattern' else "Team-Wide Uncertainty Alert"
            source = f" — source: {pattern['most_common_source']}" if pattern.get('most_common_source') else ""
            st.warning(
                f"⚠️ **{label}:** {pattern['affected_count']} of {pattern['total_engineers']} engineers "
                f"for {pattern['duration_weeks']} consecutive weeks{source}"
            )
        for blocker in aging_blockers_list:
            try:
                open_dt = datetime.strptime(blocker['open_since'], "%Y-%m-%d").strftime("%B %d, %Y")
            except Exception:
                open_dt = blocker['open_since']
            st.error(f"🔴 **Aging Blocker:** \"{blocker['description']}\" — open since {open_dt}")

        # ── Panel 1: Team Signal Status ─────────────────────────────────────
        st.markdown("## Team Signal Status")
        st.caption("Most recent signal logged per engineer")

        DELIVERY_EMOJI = {'On Track': '✅', 'At Risk': '⚠️', 'Blocked': '🔴'}
        STRESS_EMOJI = {'Low': '😌', 'Moderate': '😐', 'High': '😰'}
        GROWTH_EMOJI = {'Growing': '🌱', 'Coasting': '➡️', 'Struggling': '📉'}

        rows = []
        for engineer in engineers:
            eid = engineer['id']
            sig = signal_by_engineer.get(eid)
            flag_count = len(flags_by_engineer.get(eid, []))

            if sig:
                delivery = DELIVERY_EMOJI.get(sig['delivery_signal'], '') + ' ' + sig['delivery_signal']
                stress = STRESS_EMOJI.get(sig['stress_level'], '') + ' ' + sig['stress_level']
                growth = GROWTH_EMOJI.get(sig['growth_signal'], '') + ' ' + sig['growth_signal']
                energy = f"🔋 {sig['energy_level']}/5"
                logged = sig['logged_at'][:10]
            else:
                delivery = stress = growth = energy = "—"
                logged = "No signal yet"

            rows.append({
                'Engineer': engineer['name'],
                'Last Signal': logged,
                'Energy': energy,
                'Delivery': delivery,
                'Stress': stress,
                'Growth': growth,
                'Flags': str(flag_count) if flag_count > 0 else "—",
            })

        st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)

        st.divider()

        # ── Panel 2: Metric Status ───────────────────────────────────────────
        st.markdown("## Metric Status")
        st.caption("Latest annotation per operational metric")

        CLASS_EMOJI = {'Red': '🔴', 'Orange': '🟠', 'Amber': '⚠️'}
        metric_flags_by_id = {mf['metric_id']: mf['flag_type'] for mf in metric_flags}

        if not all_metrics:
            st.info("No metrics configured.")
        else:
            metric_rows = []
            for metric in all_metrics:
                ann = ann_by_metric.get(metric['id'])
                if ann:
                    cls = ann['classification']
                    classification = f"{CLASS_EMOJI.get(cls, '')} {cls}"
                    current_value = ann['current_value']
                    target_value = ann.get('target_value') or "—"
                    last_annotated = ann['annotated_at'][:10]
                else:
                    classification = "—"
                    current_value = "No annotation yet"
                    target_value = "—"
                    last_annotated = "Never"

                flag_type = metric_flags_by_id.get(metric['id'])
                trend = '📈' if flag_type == 'improving_trend' else ('🔴' if flag_type == 'sustained_red' else '—')

                metric_rows.append({
                    'Metric':          metric['name'],
                    'Current Value':   current_value,
                    'Target Value':    target_value,
                    'Classification':  classification,
                    'Last Annotated':  last_annotated,
                    'Trend':           trend,
                })

            st.dataframe(pd.DataFrame(metric_rows), width='stretch', hide_index=True)

        st.divider()

        # ── Panel 3: Active Flags ────────────────────────────────────────────
        st.markdown("## Active Flags")
        st.caption("Items requiring your attention right now")

        FLAG_DESCRIPTIONS = {
            'stress_trend':      "High stress",
            'uncertainty_trend': "High uncertainty",
            'delivery_trend':    "Delivery at risk",
            'energy_trend':      "Low energy trend",
        }
        METRIC_FLAG_DESCRIPTIONS = {
            'sustained_red':         "Sustained Red",
            'improving_trend':       "Improving trend",
            'sustained_improvement': "Sustained improvement",
        }

        flag_rows = []

        for flag in trend_flags:
            flag_rows.append({
                'Type':  'Engineer Signal',
                'Name':  flag['engineer_name'],
                'Flag':  FLAG_DESCRIPTIONS.get(flag['flag_type'], flag['flag_type']),
                'Since': f"{flag['duration']} weeks",
            })

        for flag in metric_flags:
            flag_rows.append({
                'Type':  'Metric',
                'Name':  flag['metric_name'],
                'Flag':  METRIC_FLAG_DESCRIPTIONS.get(flag['flag_type'], flag['flag_type']),
                'Since': f"{flag['duration']} annotations",
            })

        for blocker in aging_blockers_list:
            try:
                open_date = datetime.strptime(blocker['open_since'], "%Y-%m-%d").date()
                days_open = (datetime.today().date() - open_date).days
            except Exception:
                days_open = "?"
            desc = blocker['description']
            flag_rows.append({
                'Type':  'Blocker',
                'Name':  desc[:50] + ("..." if len(desc) > 50 else ""),
                'Flag':  "Aging blocker",
                'Since': f"{days_open} days",
            })

        for pattern in patterns:
            ptype = "Team stress" if pattern['pattern_type'] == 'stress_pattern' else "Team uncertainty"
            flag_rows.append({
                'Type':  'Team-Wide',
                'Name':  f"{pattern['affected_count']} of {pattern['total_engineers']} engineers",
                'Flag':  ptype,
                'Since': f"{pattern['duration_weeks']} weeks",
            })

        if flag_rows:
            st.dataframe(pd.DataFrame(flag_rows), width='stretch', hide_index=True)
        else:
            st.success("✅ No active flags — your team is in good shape this week.")

        st.divider()

        # ── Panel 4: Quick Actions ───────────────────────────────────────────
        st.markdown("## Quick Actions")
        st.caption("Common actions")

        qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)
        with qa_col1:
            if st.button("📝 Log Signal", width='stretch', type="primary"):
                st.switch_page("pages/signal_logging.py")
        with qa_col2:
            if st.button("📊 Annotate Metric", width='stretch'):
                st.switch_page("pages/metric_annotation.py")
        with qa_col3:
            if st.button("🚧 Log Blocker", width='stretch'):
                st.switch_page("pages/manager_blockers.py")
        with qa_col4:
            if st.button("📋 Generate Brief", width='stretch'):
                st.switch_page("pages/generate_brief.py")
        
    else:
        st.markdown("# 📊 Engineering Leadership Signal Tool")
        
        # Show warning and setup prompt
        st.error("⚠️ No Engineers Found")
        st.markdown("""
        ### You need to add engineers to your team before you can start using the tool.
        
        The Engineering Leadership Signal Tool helps you track human signals and operational context,
        but you need team members to track signals for!
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("👥 Set Up Your Team", width='stretch', type="primary"):
                st.switch_page("pages/team_setup.py")
        
        st.markdown("---")
        st.markdown("### 💡 What happens next?")
        st.markdown("""
        1. **Add engineers** to your team using the Team Setup page
        2. **Start logging signals** from your 1:1 meetings  
        3. **Annotate metrics** with human context
        4. **Generate weekly briefs** with AI-powered insights
        """)

# Main application logic
def main():
    # Initialize database if needed
    try:
        initialize_database()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()
    
    # Check if onboarding is complete
    if check_onboarding_complete():
        show_main_app()
    else:
        show_onboarding()

if __name__ == "__main__":
    main()

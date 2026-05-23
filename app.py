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
    
    # Header
    st.markdown("# 📊 Engineering Leadership Signal Tool")
    st.markdown("---")
    
    # What the tool is and why it exists
    st.markdown("## Welcome! 👋")
    st.markdown("""
    **What this tool is:** A structured way to capture the human signals behind your team's performance data.
    
    **Why it exists:** Engineering leaders are expected to explain operational metrics in business reviews, 
    but the human context gets lost. By the time the review happens, the context is gone — discussed 
    in a meeting, stored in someone's head, or buried in a Slack thread. Leadership makes decisions 
    based on numbers without the story behind them.
    
    This tool solves that by maintaining a persistent record of human signals and metric context over time.
    """)
    
    # The five signals explanation
    st.markdown("## The Five Human Signals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔋 Energy Level (1-5)")
        st.markdown("""
        **What it measures:** How present and energized is this engineer today?
        
        **Scale:** 1 = Depleted, 5 = Highly energized
        
        **Why it matters:** Energy is the foundation of sustainable performance. 
        Low energy over time indicates burnout risk or disengagement.
        """)
        
        st.markdown("### 🚀 Delivery Signal")
        st.markdown("""
        **What it measures:** Are they on track with their current commitments?
        
        **Options:** On Track, At Risk, Blocked
        
        **Why it matters:** Delivery risk needs early intervention. 
        "Blocked" requires immediate action, "At Risk" needs attention.
        """)
        
        st.markdown("### 🌱 Growth Signal")
        st.markdown("""
        **What it measures:** Are they developing professionally or showing signs of stagnation?
        
        **Options:** Growing, Coasting, Struggling
        
        **Why it matters:** Professional growth prevents stagnation and builds future capability. 
        "Struggling" may need coaching support, "Coasting" may need new challenges.
        """)
    
    with col2:
        st.markdown("### 😰 Stress Level")
        st.markdown("""
        **What it measures:** Is this engineer under pressure beyond normal levels?
        
        **Options:** Low, Moderate, High
        
        **Why it matters:** Chronic stress leads to burnout and attrition. 
        High stress requires understanding the source and appropriate management response.
        """)
        
        st.markdown("### ❓ Uncertainty Level")
        st.markdown("""
        **What it measures:** Does this engineer feel unclear about direction or priorities?
        
        **Options:** Low, Moderate, High
        
        **Why it matters:** Uncertainty paralyzes action and creates anxiety. 
        High uncertainty indicates need for clearer communication or decision-making.
        """)
    
    # How automatic trend detection works
    st.markdown("## 📈 Automatic Trend Detection")
    st.markdown("""
    This tool automatically detects patterns that might otherwise stay invisible:
    
    - **Stress Trends:** High stress for 3+ consecutive check-ins triggers an alert
    - **Uncertainty Trends:** High uncertainty for 2+ consecutive check-ins triggers an alert  
    - **Delivery Trends:** "At Risk" or "Blocked" for 2+ consecutive check-ins triggers an alert
    - **Energy Trends:** Average energy below 3 for 3+ check-ins in 30 days triggers an alert
    - **Team-wide Patterns:** When 50%+ of your team shows the same signal for extended periods
    
    These trends appear in your dashboard and weekly briefs, helping you act proactively 
    rather than reactively.
    """)
    
    # Get Started button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", width='stretch', type="primary"):
            if set_onboarding_complete():
                st.success("Welcome! Setting up your team...")
                st.rerun()
            else:
                st.error("Failed to save your progress. Please try again.")
    
    # Footer
    st.markdown("---")
    st.markdown("*This tool helps you lead with data-backed human insight.*")

def show_main_app():
    """Display the main application after onboarding"""
    st.set_page_config(
        page_title="Engineering Leadership Signal Tool",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
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

        if not all_metrics:
            st.info("No metrics configured.")
        else:
            for metric in all_metrics:
                ann = ann_by_metric.get(metric['id'])
                if ann:
                    emoji = CLASS_EMOJI.get(ann['classification'], '⬜')
                    st.markdown(f"{emoji} **{metric['name']}** — {ann['current_value']}")
                    preview = ann['explanation'][:80]
                    if len(ann['explanation']) > 80:
                        preview += "..."
                    st.caption(preview)
                else:
                    st.markdown(f"⬜ **{metric['name']}** — *No annotation yet*")
                st.markdown("")

        st.divider()

        # ── Panel 3: Active Flags ────────────────────────────────────────────
        st.markdown("## Active Flags")
        st.caption("Items requiring your attention right now")

        FLAG_LABELS = {
            'stress_trend': ('⚠️', 'stress trend'),
            'uncertainty_trend': ('⚠️', 'uncertainty trend'),
            'delivery_trend': ('🔴', 'delivery at risk'),
            'energy_trend': ('⚠️', 'low energy trend'),
        }
        METRIC_FLAG_LABELS = {
            'sustained_red': ('🔴', 'sustained red'),
            'improving_trend': ('📈', 'improving trend'),
            'sustained_improvement': ('✅', 'sustained improvement'),
        }

        has_any = bool(trend_flags or metric_flags)

        for flag in trend_flags:
            emoji, label = FLAG_LABELS.get(flag['flag_type'], ('⚠️', flag['flag_type']))
            st.markdown(f"{emoji} **{flag['engineer_name']}** — {label} ({flag['duration']} check-ins)")

        if trend_flags and metric_flags:
            st.markdown("---")

        for flag in metric_flags:
            emoji, label = METRIC_FLAG_LABELS.get(flag['flag_type'], ('⚠️', flag['flag_type']))
            st.markdown(f"{emoji} **{flag['metric_name']}** — {label} ({flag['duration']} annotations)")

        if not has_any:
            st.info("No active flags. Team is on track.")

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

import streamlit as st


NAV_ITEMS = [
    ("🏠 Dashboard",         "app.py"),
    ("📝 Log Signal",        "pages/signal_logging.py"),
    ("📊 Annotate Metric",   "pages/metric_annotation.py"),
    ("🚧 Log Blocker",       "pages/manager_blockers.py"),
    ("📋 Generate Brief",    "pages/generate_brief.py"),
    ("📈 History",           "pages/history.py"),
    ("👥 Team Setup",        "pages/team_setup.py"),
    ("ℹ️ About",             "pages/about.py"),
]


def show_navigation():
    """Render the navigation sidebar. Call this at the top of every page function."""
    with st.sidebar:
        st.markdown("# 🧭 Navigation")
        for label, target in NAV_ITEMS:
            if st.button(label, width='stretch'):
                st.switch_page(target)

        st.markdown("---")
        with st.expander("📖 Legend", expanded=False):
            st.markdown("""
**Metric Classifications**
🔴 **Red** — Genuine issue, immediate action needed
🟠 **Orange** — Contextual — looks bad but explained
⚠️ **Amber** — Temporary, resolves by known date

**Engineer Signals**
🔋 Energy: 1 = Depleted · 5 = Highly energized
Delivery: ✅ On Track / ⚠️ At Risk / 🔴 Blocked
Growth: 🌱 Growing / ➡️ Coasting / 📉 Struggling
Stress: 😌 Low / 😐 Moderate / 😰 High
Uncertainty: Low / Moderate / High

**Trend Flags**
⚠️ Active flag — sustained pattern detected
📈 Improving — moving in the right direction

**Blockers**
🔴 Aging — open 14+ days, needs escalation
🟠 Recent — being actively managed
""")

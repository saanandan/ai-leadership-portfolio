import streamlit as st


NAV_ITEMS = [
    ("🏠 Dashboard",         "app.py"),
    ("📝 Log Signal",        "pages/signal_logging.py"),
    ("📊 Annotate Metric",   "pages/metric_annotation.py"),
    ("🚧 Log Blocker",       "pages/manager_blockers.py"),
    ("📋 Generate Brief",    "pages/generate_brief.py"),
    ("📈 History",           "pages/history.py"),
    ("👥 Team Setup",        "pages/team_setup.py"),
]


def show_navigation():
    """Render the navigation sidebar. Call this at the top of every page function."""
    with st.sidebar:
        st.markdown("# 🧭 Navigation")
        for label, target in NAV_ITEMS:
            if st.button(label, width='stretch'):
                st.switch_page(target)

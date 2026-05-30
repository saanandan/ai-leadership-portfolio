import streamlit as st
import os
from dotenv import load_dotenv
from database import get_connection, initialize_database, seed_default_metrics

load_dotenv()


def show_admin():
    st.set_page_config(
        page_title="Admin — Engineering Leadership Signal Tool",
        page_icon="🔐",
    )

    st.markdown("# 🔐 Admin")
    st.markdown("---")

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    if "admin_confirm_clear" not in st.session_state:
        st.session_state.admin_confirm_clear = False
    if "admin_message" not in st.session_state:
        st.session_state.admin_message = None

    # Show persistent action message
    if st.session_state.admin_message:
        kind, text = st.session_state.admin_message
        if kind == "success":
            st.success(text)
        else:
            st.error(text)
        st.session_state.admin_message = None

    # ── Authentication ────────────────────────────────────────────────────────
    if not st.session_state.admin_authenticated:
        password = st.text_input("Password", type="password", key="admin_pw_input")
        if st.button("Login", type="primary"):
            expected = os.getenv("ADMIN_PASSWORD")
            if expected and password == expected:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password")
        return

    # ── Admin panel ───────────────────────────────────────────────────────────
    col_seed, col_clear = st.columns(2)

    with col_seed:
        if st.button("🌱 Populate Demo Data", type="primary", width="stretch"):
            from seed_mock_data import run_seed
            counts = run_seed()
            st.session_state.admin_message = (
                "success",
                f"✅ Demo data populated — "
                f"{counts['engineers']} engineers, "
                f"{counts['signals']} signals, "
                f"{counts['annotations']} annotations, "
                f"{counts['blockers']} blockers",
            )
            st.rerun()

    with col_clear:
        if not st.session_state.admin_confirm_clear:
            if st.button("🗑️ Clear All Data", width="stretch"):
                st.session_state.admin_confirm_clear = True
                st.rerun()
        else:
            st.warning("⚠️ This will permanently delete all data. Are you sure?")
            yes_col, no_col = st.columns(2)
            with yes_col:
                if st.button("Yes, delete everything", type="primary", width="stretch"):
                    initialize_database()
                    conn = get_connection()
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
                        conn.execute(f"DELETE FROM {table}")
                    conn.commit()
                    conn.close()
                    seed_default_metrics()
                    st.session_state.admin_confirm_clear = False
                    st.session_state.admin_message = (
                        "success",
                        "✅ All data cleared. Default metrics re-seeded.",
                    )
                    st.rerun()
            with no_col:
                if st.button("Cancel", width="stretch"):
                    st.session_state.admin_confirm_clear = False
                    st.rerun()


if __name__ == "__main__":
    show_admin()

import streamlit as st
from database import (
    save_blocker, get_active_blockers, get_resolved_blockers,
    detect_aging_blockers, resolve_blocker,
)
from datetime import date, datetime


ESCALATION_OPTIONS = [
    "Approval to proceed with my proposed solution",
    "Nudge someone who is not responding to me",
    "Choose between two equally good options",
    "Choose between two equally bad options",
]


def show_manager_blockers():
    """Display manager blocker logging form"""
    st.set_page_config(
        page_title="Manager Blockers - Engineering Leadership Signal Tool",
        page_icon="🚧",
        layout="wide"
    )

    if 'blocker_saved' not in st.session_state:
        st.session_state.blocker_saved = None  # ('success'|'error', text)
    if 'resolve_blocker_id' not in st.session_state:
        st.session_state.resolve_blocker_id = None

    st.markdown("# 🚧 Manager Blockers")
    st.markdown(
        "Log blockers that require your manager's involvement. "
        "Only escalate when you have exhausted your own options."
    )
    st.markdown("---")

    # Feedback banner
    if st.session_state.blocker_saved:
        kind, text = st.session_state.blocker_saved
        if kind == 'success':
            st.success(text)
        else:
            st.error(text)
        st.session_state.blocker_saved = None

    st.markdown("## Log a Blocker")

    description = st.text_input(
        "What is blocked? *",
        placeholder="Describe what you are unable to move forward on",
        help="Describe what you are unable to move forward on",
        key="bl_description",
    )

    open_since = st.date_input(
        "Open since *",
        value=date.today(),
        help="When did this blocker first appear?",
        key="bl_open_since",
    )

    what_tried = st.text_area(
        "What have you already tried? *",
        placeholder="List everything you have attempted so far...",
        help="Document everything you have already tried. This shows your manager you have exhausted your options before escalating.",
        max_chars=500,
        key="bl_what_tried",
    )

    options_remaining = st.text_area(
        "What options remain within your control? *",
        placeholder="List any remaining options you have not yet tried...",
        help="What options remain that are within your control? If none — that is when escalation is appropriate.",
        max_chars=500,
        key="bl_options_remaining",
    )

    escalation_type = st.selectbox(
        "Escalation type *",
        options=ESCALATION_OPTIONS,
        help="You should only escalate when you need an approval, a nudge, or a decision between equally weighted options.",
        key="bl_escalation_type",
    )

    specific_ask = st.text_input(
        "Specific ask *",
        placeholder="Exactly what do you need your manager to do?",
        help="Be specific. Your manager needs to know exactly what action you are asking them to take.",
        max_chars=300,
        key="bl_specific_ask",
    )
    chars_used = len(specific_ask)
    st.caption(f"{chars_used}/300 characters")

    st.markdown("---")

    if st.button("Log Blocker", type="primary"):
        errors = []

        if not description.strip():
            errors.append("'What is blocked' is required.")
        if not what_tried.strip():
            errors.append("'What have you already tried' is required.")
        if not options_remaining.strip():
            errors.append("'What options remain' is required.")
        if not escalation_type:
            errors.append("Escalation type is required.")
        if not specific_ask.strip():
            errors.append("'Specific ask' is required.")
        elif len(specific_ask.strip()) > 300:
            errors.append("'Specific ask' must be 300 characters or fewer.")

        if errors:
            for err in errors:
                st.error(f"❌ {err}")
        else:
            new_id = save_blocker(
                description=description.strip(),
                open_since=open_since,
                what_tried=what_tried.strip(),
                options_remaining=options_remaining.strip(),
                escalation_type=escalation_type,
                specific_ask=specific_ask.strip(),
            )
            if new_id:
                st.session_state.blocker_saved = (
                    'success',
                    f"✅ Blocker logged: \"{description.strip()}\""
                )
                # Clear form fields
                for key in ['bl_description', 'bl_what_tried', 'bl_options_remaining',
                            'bl_escalation_type', 'bl_specific_ask']:
                    if key in st.session_state:
                        del st.session_state[key]
            else:
                st.session_state.blocker_saved = (
                    'error',
                    "❌ Failed to save blocker. Please try again."
                )
            st.rerun()


    # ── Active Blockers ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Active Blockers")

    active_blockers = get_active_blockers()
    aging_ids = {b['id'] for b in detect_aging_blockers()}

    if not active_blockers:
        st.info("No active blockers. Nice work.")
    else:
        for blocker in active_blockers:
            bid = blocker['id']
            is_aging = bid in aging_ids

            try:
                open_dt = datetime.strptime(blocker['open_since'], "%Y-%m-%d").strftime("%B %d, %Y")
            except Exception:
                open_dt = blocker['open_since']

            # Aging badge + header
            if is_aging:
                st.warning(f"⚠️ **Aging Blocker** — open since {open_dt}")

            with st.container(border=True):
                h_col, btn_col = st.columns([5, 1])
                with h_col:
                    st.markdown(f"**{blocker['description']}**")
                    if not is_aging:
                        st.caption(f"Open since {open_dt}")
                    st.caption(f"Escalation: {blocker['escalation_type']}")
                with btn_col:
                    if st.button("Mark Resolved", key=f"resolve_btn_{bid}"):
                        st.session_state.resolve_blocker_id = bid
                        st.rerun()

                with st.expander("Details"):
                    st.markdown(f"**What I tried:** {blocker['what_tried']}")
                    st.markdown(f"**Options remaining:** {blocker['options_remaining']}")
                    st.markdown(f"**Specific ask:** {blocker['specific_ask']}")

            # Resolution form — appears inline below the selected blocker
            if st.session_state.resolve_blocker_id == bid:
                with st.container(border=True):
                    st.markdown("#### Resolve this blocker")

                    resolution_date = st.date_input(
                        "Resolution date",
                        value=date.today(),
                        key=f"res_date_{bid}",
                    )
                    resolution_desc = st.text_input(
                        "How was it resolved? *",
                        placeholder="Describe how the blocker was resolved...",
                        key=f"res_desc_{bid}",
                    )

                    c1, c2 = st.columns([1, 4])
                    with c1:
                        if st.button("Confirm Resolution", type="primary", key=f"confirm_res_{bid}"):
                            if not resolution_desc.strip():
                                st.error("❌ Please describe how it was resolved.")
                            else:
                                if resolve_blocker(bid, resolution_date, resolution_desc.strip()):
                                    st.session_state.blocker_saved = (
                                        'success',
                                        f"✅ Blocker resolved: \"{blocker['description']}\""
                                    )
                                    st.session_state.resolve_blocker_id = None
                                else:
                                    st.session_state.blocker_saved = (
                                        'error',
                                        "❌ Failed to resolve blocker. Please try again."
                                    )
                                st.rerun()
                    with c2:
                        if st.button("Cancel", key=f"cancel_res_{bid}"):
                            st.session_state.resolve_blocker_id = None
                            st.rerun()

    # ── Resolved Blockers ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Blocker History")

    resolved_blockers = get_resolved_blockers()

    if not resolved_blockers:
        st.info("No resolved blockers yet.")
    else:
        for blocker in resolved_blockers:
            try:
                open_dt = datetime.strptime(blocker['open_since'], "%Y-%m-%d").strftime("%B %d, %Y")
            except Exception:
                open_dt = blocker['open_since']

            try:
                resolved_dt = datetime.fromisoformat(blocker['resolved_at']).strftime("%B %d, %Y")
            except Exception:
                resolved_dt = blocker.get('resolved_at', '')

            with st.expander(f"✅ {blocker['description']} — resolved {resolved_dt}"):
                st.markdown(f"**Opened:** {open_dt}")
                st.markdown(f"**Escalation:** {blocker['escalation_type']}")
                st.markdown(f"**Specific ask:** {blocker['specific_ask']}")
                st.markdown(f"**What was tried:** {blocker['what_tried']}")
                st.markdown(f"**Options that remained:** {blocker['options_remaining']}")
                st.markdown(f"**How it was resolved:** {blocker['resolution_description']}")


if __name__ == "__main__":
    show_manager_blockers()

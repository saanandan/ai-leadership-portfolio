import streamlit as st
from database import (
    get_all_metrics, add_custom_metric, deactivate_metric,
    update_strategic_context, get_strategic_context_history,
    save_annotation, get_all_engineers,
    get_metric_annotations,
)
from datetime import datetime
from components.navigation import show_navigation


def show_metric_annotation():
    """Display metric management screen"""
    st.set_page_config(
        page_title="Metric Management - Engineering Leadership Signal Tool",
        page_icon="📊",
        layout="wide"
    )
    show_navigation()

    # Initialize session state
    if 'metric_action_message' not in st.session_state:
        st.session_state.metric_action_message = None  # ('success'|'error', text)
    if 'confirm_remove_id' not in st.session_state:
        st.session_state.confirm_remove_id = None
    if 'confirm_remove_name' not in st.session_state:
        st.session_state.confirm_remove_name = None

    st.markdown("# 📊 Metric Management")
    st.markdown("Manage the metrics used to track your team's engineering health.")
    st.markdown("---")

    # Show action feedback message
    if st.session_state.metric_action_message:
        kind, text = st.session_state.metric_action_message
        if kind == 'success':
            st.success(text)
        else:
            st.error(text)
        st.session_state.metric_action_message = None

    # ── Active Metrics List ───────────────────────────────────────────────────
    st.markdown("## Active Metrics")

    metrics = get_all_metrics()

    if not metrics:
        st.info("No active metrics found.")
    else:
        for metric in metrics:
            mid = metric['id']

            # Header row: name, badge, remove button
            col_name, col_badge, col_remove = st.columns([5, 1, 1])
            with col_name:
                desc = f" — {metric['description']}" if metric['description'] else ""
                st.markdown(f"**{metric['name']}**{desc}")
            with col_badge:
                if metric['is_default']:
                    st.caption("default")
            with col_remove:
                if st.button("Remove", key=f"remove_{mid}"):
                    st.session_state.confirm_remove_id = mid
                    st.session_state.confirm_remove_name = metric['name']
                    st.rerun()

            # Strategic context expander
            with st.expander("Strategic Context"):
                st.caption(
                    "Use this for standing context that explains why this metric may look a "
                    "certain way over an extended period — such as resource constraints, system "
                    "retirement, or shifting priorities."
                )

                current_context = metric['strategic_context'] or ""
                updated_at = metric['strategic_context_updated_at']

                # Last updated + View History toggle
                if updated_at:
                    try:
                        updated_dt = datetime.fromisoformat(updated_at).strftime("%B %d, %Y at %I:%M %p")
                    except ValueError:
                        updated_dt = updated_at

                    hist_key = f"show_history_{mid}"
                    if hist_key not in st.session_state:
                        st.session_state[hist_key] = False

                    ts_col, hist_col = st.columns([3, 1])
                    with ts_col:
                        st.caption(f"Last updated: {updated_dt}")
                    with hist_col:
                        label = "Hide History" if st.session_state[hist_key] else "View History"
                        if st.button(label, key=f"hist_btn_{mid}"):
                            st.session_state[hist_key] = not st.session_state[hist_key]
                            st.rerun()

                    if st.session_state[hist_key]:
                        history = get_strategic_context_history(mid)
                        if not history:
                            st.info("No history yet.")
                        else:
                            for entry in history:
                                try:
                                    changed = datetime.fromisoformat(entry['changed_at']).strftime("%B %d, %Y at %I:%M %p")
                                except ValueError:
                                    changed = entry['changed_at']
                                st.markdown(f"**{changed}**")
                                st.markdown(entry['new_context'] or "*(cleared)*")
                                st.markdown("---")

                new_context = st.text_area(
                    "Strategic Context",
                    value=current_context,
                    placeholder="Describe any standing context that affects this metric...",
                    key=f"ctx_{mid}",
                    label_visibility="collapsed",
                )

                if st.button("Save Context", key=f"save_ctx_{mid}"):
                    trimmed = new_context.strip()
                    if update_strategic_context(mid, trimmed or None):
                        st.session_state.metric_action_message = (
                            'success',
                            f"✅ Strategic context updated for '{metric['name']}'."
                        )
                    else:
                        st.session_state.metric_action_message = (
                            'error',
                            f"❌ Failed to update context for '{metric['name']}'. Please try again."
                        )
                    st.rerun()

            st.markdown("")  # breathing room between metrics

    # ── Removal confirmation dialog ───────────────────────────────────────────
    if st.session_state.confirm_remove_id is not None:
        st.markdown("---")
        st.warning(
            f"**Remove '{st.session_state.confirm_remove_name}'?**  \n"
            "Removing this metric will hide it from future annotations but all historical data will be preserved."
        )

        col_confirm, col_cancel, _ = st.columns([1, 1, 4])

        with col_confirm:
            if st.button("Yes, remove it", type="primary", width='stretch'):
                success = deactivate_metric(st.session_state.confirm_remove_id)
                if success:
                    st.session_state.metric_action_message = (
                        'success',
                        f"✅ '{st.session_state.confirm_remove_name}' has been removed. Historical data is preserved."
                    )
                else:
                    st.session_state.metric_action_message = (
                        'error',
                        f"❌ Failed to remove '{st.session_state.confirm_remove_name}'. Please try again."
                    )
                st.session_state.confirm_remove_id = None
                st.session_state.confirm_remove_name = None
                st.rerun()

        with col_cancel:
            if st.button("Cancel", width='stretch'):
                st.session_state.confirm_remove_id = None
                st.session_state.confirm_remove_name = None
                st.rerun()

    # ── Add Custom Metric Form ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Add Custom Metric")

    with st.form("add_metric_form", clear_on_submit=True):
        new_name = st.text_input(
            "Metric Name *",
            placeholder="e.g. Test Coverage",
            help="Required. Must be unique.",
        )
        new_description = st.text_area(
            "Description (Optional)",
            placeholder="What does this metric measure?",
            max_chars=300,
        )

        submitted = st.form_submit_button("Add Metric", type="primary")

    if submitted:
        name_clean = new_name.strip()
        if not name_clean:
            st.error("❌ Metric name is required.")
        else:
            # Duplicate check against active metrics
            existing_names = {m['name'].lower() for m in metrics}
            if name_clean.lower() in existing_names:
                st.error(f"❌ A metric named '{name_clean}' already exists.")
            else:
                desc_clean = new_description.strip() or None
                new_id = add_custom_metric(name_clean, desc_clean)
                if new_id:
                    st.session_state.metric_action_message = (
                        'success',
                        f"✅ Metric '{name_clean}' added successfully."
                    )
                else:
                    st.session_state.metric_action_message = (
                        'error',
                        "❌ Failed to add metric. Please try again."
                    )
                st.rerun()


    # ── Annotation Form ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Log Metric Annotation")
    st.markdown("Record the current state of a metric with context for leadership.")

    if not metrics:
        st.info("Add at least one active metric above before logging an annotation.")
    else:
        CLASSIFICATION_OPTIONS = [
            "🔴 Red — Genuine Red: this is a real problem that needs immediate action",
            "🟠 Orange — Contextual Red: looks bad but here is why it is not alarming",
            "⚠️ Amber — Temporary Red: will resolve by a specific date because of a known reason",
        ]
        CLASSIFICATION_STORED = {"🔴": "Red", "🟠": "Orange", "⚠️": "Amber"}

        ann_metric = st.selectbox(
            "Metric *",
            options=metrics,
            format_func=lambda m: m['name'],
            help="Select the metric you want to annotate",
            key="ann_metric",
        )

        ann_value = st.text_input(
            "Current Value *",
            placeholder="e.g. 60%, 12 open vulns, 94%",
            help="Enter the current value of this metric e.g. 60%, 12 open vulns, 94%",
            key="ann_value",
        )

        ann_classification = st.selectbox(
            "Classification *",
            options=CLASSIFICATION_OPTIONS,
            help="Not all red metrics are equally urgent. This classification helps leadership understand what actually needs attention.",
            key="ann_classification",
        )

        ann_explanation = st.text_area(
            "Plain English Explanation *",
            placeholder="Explain the context behind this metric in plain English...",
            help="Explain the context behind this metric in plain English. This becomes part of your weekly brief.",
            max_chars=1000,
            key="ann_explanation",
        )

        # Derive which colour was chosen
        chosen_colour = ann_classification[:2].strip()
        is_red = chosen_colour == "🔴"
        is_orange_or_amber = chosen_colour in ("🟠", "⚠️")

        # Conditional: remediation owner (Red only)
        ann_owner_id = None
        if is_red:
            engineers = get_all_engineers()
            if engineers:
                ann_owner = st.selectbox(
                    "Remediation Owner *",
                    options=engineers,
                    format_func=lambda e: e['name'],
                    help="Who on your team owns the fix? Accountability drives resolution.",
                    key="ann_owner",
                )
                ann_owner_id = ann_owner['id']
            else:
                st.warning("No engineers found. Add engineers in Team Setup to assign a remediation owner.")

        # Conditional: expected resolution date (Orange or Amber only)
        ann_resolution_date = None
        if is_orange_or_amber:
            ann_resolution_date = st.date_input(
                "Expected Resolution Date",
                help="When do you expect this metric to normalize? Giving a date builds credibility with leadership.",
                key="ann_resolution_date",
            )

        if st.button("Submit Annotation", type="primary", key="ann_submit"):
            errors = []

            if ann_metric is None:
                errors.append("Metric is required.")
            if not ann_value.strip():
                errors.append("Current value is required.")
            if not ann_classification:
                errors.append("Classification is required.")
            if not ann_explanation.strip():
                errors.append("Plain English explanation is required.")
            if is_red and ann_owner_id is None:
                errors.append("Remediation owner is required when classification is Red.")

            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                stored_class = CLASSIFICATION_STORED[chosen_colour]
                new_id = save_annotation(
                    metric_id=ann_metric['id'],
                    current_value=ann_value.strip(),
                    classification=stored_class,
                    explanation=ann_explanation.strip(),
                    remediation_owner_id=ann_owner_id,
                    expected_resolution_date=str(ann_resolution_date) if ann_resolution_date else None,
                )
                if new_id:
                    st.session_state.metric_action_message = (
                        'success',
                        f"✅ Annotation saved — **{ann_metric['name']}** classified as **{stored_class}**."
                    )
                else:
                    st.session_state.metric_action_message = (
                        'error',
                        "❌ Failed to save annotation. Please try again."
                    )
                st.rerun()


    # ── Annotation History ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Annotation History")

    if not metrics:
        st.info("No active metrics to view history for.")
    else:
        CLASS_EMOJI = {'Red': '🔴', 'Orange': '🟠', 'Amber': '⚠️'}

        hist_metric = st.selectbox(
            "Select Metric",
            options=metrics,
            format_func=lambda m: m['name'],
            key="hist_metric",
        )

        if hist_metric:
            # Strategic context banner
            if hist_metric.get('strategic_context'):
                try:
                    updated_dt = datetime.fromisoformat(
                        hist_metric['strategic_context_updated_at']
                    ).strftime("%B %d, %Y")
                except Exception:
                    updated_dt = hist_metric.get('strategic_context_updated_at', '')
                st.info(
                    f"**Strategic Context** (as of {updated_dt})\n\n"
                    f"{hist_metric['strategic_context']}"
                )

            annotations = get_metric_annotations(hist_metric['id'])

            if not annotations:
                st.info("No annotations logged for this metric yet.")
            else:
                baseline = annotations[:3]  # three most recent (already newest-first)
                rest = annotations[3:]

                st.markdown(f"### Last {len(baseline)} annotation(s) — baseline comparison")
                for i, ann in enumerate(baseline):
                    try:
                        ann_dt = datetime.fromisoformat(ann['annotated_at']).strftime("%B %d, %Y at %I:%M %p")
                    except Exception:
                        ann_dt = ann['annotated_at']

                    cls = ann['classification']
                    emoji = CLASS_EMOJI.get(cls, '')

                    label = "Most recent" if i == 0 else f"{i + 1} annotations ago"
                    with st.container(border=True):
                        h_col, d_col = st.columns([3, 2])
                        with h_col:
                            st.markdown(f"**{emoji} {cls}** — {ann['current_value']}")
                            st.caption(f"{label} · {ann_dt}")
                        with d_col:
                            if ann.get('remediation_owner_name'):
                                st.caption(f"Owner: {ann['remediation_owner_name']}")
                            if ann.get('expected_resolution_date'):
                                st.caption(f"Expected resolution: {ann['expected_resolution_date']}")
                        st.markdown(ann['explanation'])

                if rest:
                    st.markdown("### Earlier annotations")
                    for ann in rest:
                        try:
                            ann_dt = datetime.fromisoformat(ann['annotated_at']).strftime("%B %d, %Y at %I:%M %p")
                        except Exception:
                            ann_dt = ann['annotated_at']

                        cls = ann['classification']
                        emoji = CLASS_EMOJI.get(cls, '')

                        with st.expander(f"{emoji} {cls} — {ann['current_value']} · {ann_dt}"):
                            st.markdown(ann['explanation'])
                            if ann.get('remediation_owner_name'):
                                st.caption(f"Owner: {ann['remediation_owner_name']}")
                            if ann.get('expected_resolution_date'):
                                st.caption(f"Expected resolution: {ann['expected_resolution_date']}")


if __name__ == "__main__":
    show_metric_annotation()

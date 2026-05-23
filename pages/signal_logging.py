import streamlit as st
from database import get_all_engineers, save_signal, delete_signal, get_signals
from datetime import datetime, timedelta, date
from components.navigation import show_navigation

def show_signal_logging():
    """Display signal logging screen"""
    st.set_page_config(
        page_title="Signal Logging - Engineering Leadership Signal Tool",
        page_icon="📝",
        layout="wide"
    )
    show_navigation()
    
    # Initialize session state
    if 'signal_saved' not in st.session_state:
        st.session_state.signal_saved = False
    if 'saved_signal_id' not in st.session_state:
        st.session_state.saved_signal_id = None
    if 'saved_signal_time' not in st.session_state:
        st.session_state.saved_signal_time = None
    if 'saved_engineer_name' not in st.session_state:
        st.session_state.saved_engineer_name = None
    
    st.markdown("# 📝 Signal Logging")
    st.markdown("Log human signals captured during 1:1 meetings with individual engineers.")
    st.markdown("---")
    
    # Get engineers for dropdown
    engineers = get_all_engineers()
    if not engineers:
        st.error("⚠️ No engineers found. Please add engineers in Team Setup first.")
        st.stop()
    
    # Signal logging form
    st.markdown("## Log New Signal")
    
    # Engineer selection
    selected_engineer = st.selectbox(
        "Select Engineer *",
        options=[(engineer['id'], engineer['name']) for engineer in engineers],
        format_func=lambda x: f"{x[0]} - {x[1]}",
        help="Choose the engineer this signal is for",
        key="engineer_select"
    )
    
    # Energy level (1-5)
    st.markdown("### 🔋 Energy Level (1-5)")
    energy_level = st.slider(
        "Energy Level",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        help="How present and energized is this engineer today? 1 = depleted, 5 = highly energized",
        key="energy_level"
    )
    
    st.markdown("""
    **What it measures:** How present and energized is this engineer today?
    
    **Scale:** 1 = Depleted, 5 = Highly energized
    
    **Why it matters:** Energy is the foundation of sustainable performance. 
    Low energy over time indicates burnout risk or disengagement.
    """)
    
    # Delivery signal
    st.markdown("### 🚀 Delivery Signal")
    delivery_signal = st.selectbox(
        "Delivery Signal *",
        options=["On Track", "At Risk", "Blocked"],
        help="Are they on track with their current commitments?",
        key="delivery_signal"
    )
    
    st.markdown("""
    **Options:** On Track, At Risk, Blocked
    
    **Why it matters:** Delivery risk needs early intervention. 
    "Blocked" requires immediate action, "At Risk" needs attention.
    """)
    
    # Growth signal
    st.markdown("### 🌱 Growth Signal")
    growth_signal = st.selectbox(
        "Growth Signal *",
        options=["Growing", "Coasting", "Struggling"],
        help="Are they developing professionally or showing signs of stagnation?",
        key="growth_signal"
    )
    
    st.markdown("""
    **Options:** Growing, Coasting, Struggling
    
    **Why it matters:** Professional growth prevents stagnation and builds future capability. 
    "Struggling" may need coaching support, "Coasting" may need new challenges.
    """)
    
    # Stress level
    st.markdown("### 😰 Stress Level")
    stress_level = st.selectbox(
        "Stress Level *",
        options=["Low", "Moderate", "High"],
        help="Is this engineer under pressure beyond normal levels?",
        key="stress_level"
    )
    
    st.markdown("""
    **Options:** Low, Moderate, High
    
    **Why it matters:** Chronic stress leads to burnout and attrition. 
    High stress requires understanding of source and appropriate management response.
    """)
    
    # Stress source (conditional)
    stress_source = None
    if stress_level in ["Moderate", "High"]:
        st.markdown("#### Stress Source *")
        stress_source = st.selectbox(
            "Stress Source *",
            options=["Workload", "Team dynamics", "Organizational pressure", "Personal"],
            help="What is driving the stress? This determines your management response.",
            key="stress_source"
        )
        
        st.markdown("""
        **What it is:** Workload, Team dynamics, Organizational pressure, Personal
        
        **Why it matters:** Different sources require different management approaches. 
        Understanding the source helps you provide the right support.
        """)
    
    # Uncertainty level
    st.markdown("### ❓ Uncertainty Level")
    uncertainty_level = st.selectbox(
        "Uncertainty Level *",
        options=["Low", "Moderate", "High"],
        help="Does this engineer feel unclear about direction or priorities?",
        key="uncertainty_level"
    )
    
    st.markdown("""
    **Options:** Low, Moderate, High
    
    **Why it matters:** Uncertainty paralyzes action and creates anxiety. 
    High uncertainty indicates need for clearer communication or decision-making.
    """)
    
    # Uncertainty source (conditional)
    uncertainty_source = None
    if uncertainty_level in ["Moderate", "High"]:
        st.markdown("#### Uncertainty Source *")
        uncertainty_source = st.selectbox(
            "Uncertainty Source *",
            options=["Team direction", "Company direction", "Shifting priorities", "Role clarity"],
            help="What specifically is unclear? This helps you decide whether to act locally or escalate.",
            key="uncertainty_source"
        )
        
        st.markdown("""
        **What it is:** Team direction, Company direction, Shifting priorities, Role clarity
        
        **Why it matters:** Different sources require different solutions. 
        Team direction needs clarity, company direction needs escalation, 
        shifting priorities need alignment, role clarity needs coaching.
        """)
    
    # Free text observation
    st.markdown("### 📝 Observation")
    observation = st.text_area(
        "Observation (Optional)",
        placeholder="One thing you noticed in this 1:1 that isn't captured above...",
        help="One thing you noticed in this 1:1 that isn't captured above. Optional.",
        max_chars=500,
        key="observation"
    )
    
    st.markdown("""
    **What it is:** A free-form observation from the meeting.
    
    **Why it matters:** Captures qualitative insights that don't fit in structured fields.
    
    **Guidelines:** Keep it brief, specific, and actionable.
    """)
    
    # Submit button
    st.markdown("---")
    
    # Show post-save buttons if a signal was just saved
    if st.session_state.signal_saved:
        logged_at = st.session_state.saved_signal_time.strftime("%B %d, %Y at %I:%M %p")
        st.success(f"✅ Signal logged for **{st.session_state.saved_engineer_name}** on {logged_at}")
        
        # Check if within 10-minute window for undo
        time_since_save = datetime.now() - st.session_state.saved_signal_time
        can_undo = time_since_save < timedelta(minutes=10)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("� Log Another Signal", width='stretch', type="primary"):
                    # Clear session state and form
                    st.session_state.signal_saved = False
                    st.session_state.saved_signal_id = None
                    st.session_state.saved_signal_time = None
                    st.session_state.saved_engineer_name = None
                    # Clear all form keys
                    for key in st.session_state.keys():
                        if key in ['engineer_select', 'energy_level', 'delivery_signal', 'growth_signal', 
                                  'stress_level', 'stress_source', 'uncertainty_level', 'uncertainty_source', 'observation']:
                            del st.session_state[key]
                    st.rerun()
            
            with col_b:
                if can_undo:
                    if st.button("↩️ Undo this entry", width='stretch'):
                        if st.session_state.saved_signal_id:
                            if delete_signal(st.session_state.saved_signal_id):
                                st.success("✅ Signal deleted successfully!")
                                st.session_state.signal_saved = False
                                st.session_state.saved_signal_id = None
                                st.session_state.saved_signal_time = None
                                st.session_state.saved_engineer_name = None
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete signal.")
                else:
                    st.info("⏱️ Undo window expired (10 minutes)")
        
        with col1:
            st.markdown("&nbsp;")
        
        with col3:
            st.markdown("&nbsp;")
    else:
        # Show normal form buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🔙 Cancel", width='stretch'):
                    # Clear all form fields by deleting their session state
                    for key in st.session_state.keys():
                        if key in ['engineer_select', 'energy_level', 'delivery_signal', 'growth_signal', 
                                  'stress_level', 'stress_source', 'uncertainty_level', 'uncertainty_source', 'observation']:
                            del st.session_state[key]
                    st.rerun()
            
            with col_b:
                if st.button("�💾 Save Signal", width='stretch', type="primary"):
                    # Validation
                    if not selected_engineer:
                        st.error("❌ Please select an engineer.")
                        st.stop()
                    
                    # Prepare signal data
                    signal_data = {
                        'engineer_id': selected_engineer[0],
                        'energy_level': energy_level,
                        'delivery_signal': delivery_signal,
                        'growth_signal': growth_signal,
                        'stress_level': stress_level,
                        'stress_source': stress_source if stress_level in ["Moderate", "High"] else None,
                        'uncertainty_level': uncertainty_level,
                        'uncertainty_source': uncertainty_source if uncertainty_level in ["Moderate", "High"] else None,
                        'observation': observation.strip() if observation.strip() else None
                    }
                    
                    new_id = save_signal(
                        engineer_id=signal_data['engineer_id'],
                        energy_level=signal_data['energy_level'],
                        delivery_signal=signal_data['delivery_signal'],
                        growth_signal=signal_data['growth_signal'],
                        stress_level=signal_data['stress_level'],
                        stress_source=signal_data['stress_source'],
                        uncertainty_level=signal_data['uncertainty_level'],
                        uncertainty_source=signal_data['uncertainty_source'],
                        observation=signal_data['observation']
                    )

                    if new_id is None:
                        st.error("❌ Failed to save signal. Please try again.")
                        st.stop()

                    st.session_state.saved_signal_id = new_id
                    st.session_state.saved_signal_time = datetime.now()
                    st.session_state.saved_engineer_name = selected_engineer[1]
                    st.session_state.signal_saved = True
                    st.rerun()
        
        with col1:
            st.markdown("&nbsp;")
        
        with col3:
            st.markdown("&nbsp;")

    # ── Signal History ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Signal History")

    # Filters
    with st.expander("Filters", expanded=True):
        f_col1, f_col2 = st.columns(2)

        with f_col1:
            engineer_options = [("", "All Engineers")] + [(e['id'], e['name']) for e in engineers]
            filter_engineer = st.selectbox(
                "Engineer",
                options=engineer_options,
                format_func=lambda x: x[1],
                key="history_engineer"
            )

            filter_delivery = st.selectbox(
                "Delivery Signal",
                options=["All", "On Track", "At Risk", "Blocked"],
                key="history_delivery"
            )

        with f_col2:
            today = date.today()
            filter_start = st.date_input(
                "From date",
                value=today.replace(day=1),
                key="history_start"
            )
            filter_end = st.date_input(
                "To date",
                value=today,
                key="history_end"
            )

            filter_stress = st.selectbox(
                "Stress Level",
                options=["All", "Low", "Moderate", "High"],
                key="history_stress"
            )

        filter_uncertainty = st.selectbox(
            "Uncertainty Level",
            options=["All", "Low", "Moderate", "High"],
            key="history_uncertainty"
        )

    signals = get_signals(
        engineer_id=filter_engineer[0] if filter_engineer[0] != "" else None,
        start_date=filter_start,
        end_date=filter_end,
        delivery_signal=filter_delivery if filter_delivery != "All" else None,
        stress_level=filter_stress if filter_stress != "All" else None,
        uncertainty_level=filter_uncertainty if filter_uncertainty != "All" else None,
    )

    if not signals:
        st.info("No signals match the selected filters.")
    else:
        rows = []
        for s in signals:
            logged_dt = s['logged_at']
            if isinstance(logged_dt, str):
                try:
                    logged_dt = datetime.fromisoformat(logged_dt).strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    pass
            rows.append({
                "Date": logged_dt,
                "Engineer": s['engineer_name'],
                "Energy": s['energy_level'],
                "Delivery": s['delivery_signal'],
                "Growth": s['growth_signal'],
                "Stress": s['stress_level'],
                "Uncertainty": s['uncertainty_level'],
                "Observation": s['observation'] or "",
            })

        st.dataframe(rows, width='stretch', hide_index=True)


if __name__ == "__main__":
    show_signal_logging()

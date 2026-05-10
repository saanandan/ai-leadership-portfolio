import streamlit as st
from database import get_all_engineers, add_engineer, deactivate_engineer

def show_team_setup():
    """Display the team setup screen"""
    st.set_page_config(
        page_title="Team Setup - Engineering Leadership Signal Tool",
        page_icon="👥",
        layout="wide"
    )
    
    st.markdown("# 👥 Team Setup")
    st.markdown("Add and manage your engineering team members here.")
    st.markdown("---")
    
    # Add Engineer Form
    st.markdown("## Add New Engineer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        engineer_name = st.text_input(
            "Engineer Name *",
            placeholder="Enter engineer name",
            help="The full name of the engineer you want to add"
        )
        
        engineer_role = st.text_input(
            "Role (Optional)",
            placeholder="e.g., Senior Software Engineer, DevOps Engineer",
            help="The role or title of the engineer (optional)"
        )
    
    with col2:
        st.markdown("&nbsp;")  # Add some space
        st.markdown("&nbsp;")
        st.markdown("&nbsp;")
        
        add_button = st.button(
            "➕ Add Engineer",
            use_container_width=True,
            type="primary",
            disabled=not engineer_name.strip()
        )
    
    # Handle Add Engineer
    if add_button:
        if engineer_name.strip():
            if add_engineer(engineer_name.strip(), engineer_role.strip() if engineer_role.strip() else None):
                st.success(f"✅ Engineer '{engineer_name.strip()}' added successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to add engineer. Please try again.")
        else:
            st.error("❌ Engineer name is required.")
    
    # Current Team Members
    st.markdown("---")
    st.markdown("## Current Team Members")
    
    engineers = get_all_engineers()
    
    if engineers:
        st.write(f"**{len(engineers)} active engineer(s)**")
        
        for i, engineer in enumerate(engineers):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"### {engineer['name']}")
                    if engineer.get('role') and engineer['role'].strip():
                        st.markdown(f"🏷️ {engineer['role']}")
                    else:
                        st.markdown("🏷️ *No role specified*")
                
                with col2:
                    st.markdown(f"*Added: {engineer['created_at'][:10]}*")
                
                with col3:
                    remove_key = f"remove_{engineer['id']}"
                    if st.button(
                        "🗑️ Remove",
                        key=remove_key,
                        help="Deactivate this engineer (won't delete historical data)",
                        use_container_width=True
                    ):
                        if deactivate_engineer(engineer['id']):
                            st.success(f"✅ Engineer '{engineer['name']}' deactivated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to deactivate engineer. Please try again.")
                
                if i < len(engineers) - 1:
                    st.markdown("---")
    else:
        st.info("📝 No engineers added yet. Use the form above to add your first team member.")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 💡 Notes")
    st.markdown("""
    - **Name is required** - This is how engineers will be identified in signals and reports
    - **Role is optional** - Helps you remember each engineer's position on the team
    - **Remove vs Delete** - Removing an engineer deactivates them (sets active=0) but preserves all historical signal data
    - **At least one engineer** is required before you can start logging signals
    """)
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            st.switch_page("app.py")

if __name__ == "__main__":
    show_team_setup()

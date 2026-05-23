import streamlit as st
from database import get_connection, get_all_engineers, initialize_database
from dotenv import load_dotenv
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
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
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
    with st.sidebar:
        st.markdown("# 🧭 Navigation")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            st.rerun()
        
        if st.button("📝 Signal Logging", use_container_width=True):
            st.switch_page("pages/signal_logging.py")

        if st.button("📊 Metric Annotation", use_container_width=True):
            st.switch_page("pages/metric_annotation.py")

        if st.button("🚧 Manager Blockers", use_container_width=True):
            st.switch_page("pages/manager_blockers.py")

        if st.button("📋 Generate Brief", use_container_width=True):
            st.switch_page("pages/generate_brief.py")

        if st.button("📈 History", use_container_width=True):
            st.switch_page("pages/history.py")

        if st.button("👥 Team Setup", use_container_width=True):
            st.switch_page("pages/team_setup.py")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Actions")
        st.markdown("*More features coming soon...*")
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        if st.button("🔄 Reset Onboarding", use_container_width=True, help="For testing only"):
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
        st.markdown("Welcome back! Your dashboard will appear here.")
        
        st.success(f"Found {len(engineers)} active engineers in your team.")
        
        # Display current team
        st.markdown("## 👥 Your Team")
        cols = st.columns(min(3, len(engineers)))
        
        for i, engineer in enumerate(engineers):
            with cols[i % 3]:
                st.markdown(f"### {engineer['name']}")
                if engineer.get('role') and engineer['role'].strip():
                    st.markdown(f"🏷️ {engineer['role']}")
                else:
                    st.markdown("🏷️ *No role specified*")
        
        # Placeholder for future dashboard features
        st.markdown("---")
        st.markdown("## 🚀 Coming Soon")
        st.markdown("""
        - **Signal Logging** - Capture human signals from 1:1 meetings
        - **Metrics Annotation** - Add context to operational metrics  
        - **Weekly Briefs** - AI-generated leadership insights
        - **Trend Detection** - Automatic pattern recognition
        - **Historical Analysis** - Team evolution over time
        """)
        
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
            if st.button("👥 Set Up Your Team", use_container_width=True, type="primary"):
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

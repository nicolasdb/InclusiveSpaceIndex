"""
Sidebar component for displaying score overview.
"""
import logging
import streamlit as st
from utils.styles import apply_style
from utils.scoring import MAX_POINTS_PER_QUESTION
from utils.state import get_completion_status, is_assessment_complete

# Configure logging
logger = logging.getLogger(__name__)

def handle_submit():
    """Handle submit button click."""
    if is_assessment_complete():
        logger.debug("Assessment completed, transitioning to results phase")
        st.session_state.phase = "results"

def display_score_overview(scores, df):
    """
    Display score overview in sidebar.
    
    Args:
        scores: Dictionary containing score information
        df: DataFrame containing questions data
    """
    with st.sidebar:
        # Dashboard title
        # st.title("📊 Dashboard")
        
        # Display total score
        st.markdown(f'<div class="{apply_style("score")}">', unsafe_allow_html=True)
        st.metric(
            "Total Score",
            f"{scores['total_score']}/{scores['total_max']} points",
            help="Maximum score is 8 points per question"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display progress bar (without text)
        completed, total, percentage = get_completion_status()
        st.progress(percentage / 100)
        
        # Only show submit button in assessment phase
        if st.session_state.phase == "assessment":
            st.markdown("---")
            submit_button = st.button(
                "📤 Submit Assessment",
                type="primary",
                on_click=handle_submit
            )

def display_reset_button():
    """Display reset button and handle reset action."""
    from utils.state import reset_responses
    
    # Only show/enable reset in assessment phase
    if st.session_state.phase == "assessment":
        if st.sidebar.button("🔄 Reset Assessment", type="secondary", help="Clear all responses"):
            logger.debug("Resetting assessment")
            reset_responses()
            st.session_state.phase = "assessment"  # Ensure we stay in assessment phase
    else:
        # Disabled button in results phase
        st.sidebar.button("🔄 Reset Assessment", type="secondary", disabled=True)

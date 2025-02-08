"""
Main Streamlit application for the maturity assessment.
"""
import os
import logging
import streamlit as st
from dotenv import load_dotenv

from utils.data_loader import load_questions
from utils.styles import inject_custom_css
from utils.state import init_session_state, update_scores
from components.sidebar import display_score_overview, display_reset_button
from components.questions import display_sections
from components.results import display_results_tab

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_environment():
    """Initialize environment variables and connections."""
    # Load environment variables
    load_dotenv()
    
    # Check Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        st.warning("⚠️ Supabase configuration not found. Some features may be limited.")
        logger.warning("Supabase environment variables not set")

def main():
    """Main function to run the Streamlit application."""
    # Initialize environment
    init_environment()
    
    # Page config
    st.set_page_config(
        page_title="Maturity Assessment Tool",
        page_icon="📊",
        layout="wide",
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    try:
        # Initialize session state
        init_session_state()
        
        # Initialize phase if not set
        if 'phase' not in st.session_state:
            st.session_state.phase = "assessment"
        
        # Main title with description
        st.title("🎯 Maturity Assessment Tool")
        st.markdown("""
            This tool helps you assess your organization's maturity level across different areas.
            Select a section and answer the questions to get a detailed analysis.
        """)
        
        # Load questions using enhanced data loader
        logger.debug("Loading questions")
        df = load_questions()
        logger.debug(f"Loaded {len(df)} questions")
        
        # Calculate current scores
        scores = update_scores(df)
        
        # Display score overview in sidebar
        display_score_overview(scores, df)
        
        # Show reset button only in assessment phase
        if st.session_state.phase == "assessment":
            display_reset_button()
        
        # Handle different phases
        if st.session_state.phase == "assessment":
            # Assessment phase - display sections as tabs
            display_sections(df)
        else:
            # Results phase
            display_results_tab(df, scores)
            
        # Debug information
        if st.query_params.get("debug", [False])[0]:
            st.write("Debug - Current responses:", st.session_state.responses)
            st.write("Debug - Current scores:", scores)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        st.error("⚠️ An error occurred while loading the application")
        st.error(f"Error details: {str(e)}")
        st.error("Please check the application logs for more information.")

if __name__ == "__main__":
    main()

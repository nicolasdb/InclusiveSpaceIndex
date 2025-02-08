"""
Results component for displaying assessment results and visualizations.
"""
import logging
import streamlit as st
import pandas as pd
from typing import Dict, Any
from utils.styles import apply_style
from utils.visualization import ChartGenerator
from utils.supabase import supabase
from utils.validators import validate_email
from utils.scoring import OPTION_SCORES, MAX_POINTS_PER_QUESTION

# Configure logging
logger = logging.getLogger(__name__)

def generate_csv_data(df, responses):
    """
    Generate detailed CSV data from assessment responses.
    
    Args:
        df: DataFrame containing questions data
        responses: Dictionary of responses for each question
        
    Returns:
        str: CSV data as string
    """
    # Create detailed results with all questions
    results_data = []
    for idx, row in df.iterrows():
        selected_idx = responses.get(str(idx), 0)  # Get response (default 0)
        results_data.append({
            'Question Number': row['question_number'],
            'Section': row['section'],
            'Question': row['question'],
            'Selected Option': row[f'option{selected_idx + 1}'],
            'Score': OPTION_SCORES[selected_idx],
            'Maximum Score': MAX_POINTS_PER_QUESTION,
            'Option Selected': selected_idx + 1,  # Human-readable option number (1-5)
            'Total Options': 5
        })
    
    # Convert to DataFrame and then to CSV
    results_df = pd.DataFrame(results_data)
    return results_df.to_csv(index=False)

def handle_email_change():
    """Handle email input changes and validate previous results."""
    email = st.session_state.export_email
    
    if email and validate_email(email):
        # Check for previous results
        previous_results = supabase.check_previous_results(email)
        if previous_results:
            st.session_state.previous_results = previous_results
            # Get user preferences
            prefs = supabase.get_user_preferences(email)
            st.session_state.mailing_list = prefs["mailing_list"]
            st.session_state.data_sharing = prefs["data_sharing"]
            st.session_state.email_valid = True
        else:
            st.session_state.previous_results = None
            st.session_state.mailing_list = False
            st.session_state.data_sharing = False
            st.session_state.email_valid = True
    else:
        st.session_state.email_valid = False
        st.session_state.previous_results = None
        st.session_state.mailing_list = False
        st.session_state.data_sharing = False

def handle_preferences_update(email: str, mailing_list: bool, data_sharing: bool, scores: Dict[str, Any]):
    """Handle updating user preferences and data storage."""
    if supabase.update_preferences(email, mailing_list, data_sharing):
        if data_sharing:
            # Store results with responses and totals
            if supabase.store_results(
                email=email,
                responses=st.session_state.responses,
                total_score=scores['total_score'],
                total_max=scores['total_max']
            ):
                st.success("Preferences updated and results saved!")
            else:
                st.error("Error saving results")
        else:
            st.success("Preferences updated!")
    else:
        st.error("Error updating preferences")

def display_results_tab(df, scores):
    """
    Display the complete results tab with side-by-side layout.
    
    Args:
        df: DataFrame containing questions data
        scores: Dictionary containing score information
    """
    
    # Create two columns for side-by-side layout
    col1, col2 = st.columns([0.6, 0.4])  # 60% for chart, 40% for export
    
    with col1:
        # Display radar chart
        st.markdown("### Assessment Results")
        chart_generator = ChartGenerator()
        
        # Show previous results if available
        if st.session_state.get('previous_results'):
            fig = chart_generator.create_radar_chart(scores, df, st.session_state.previous_results)
        else:
            fig = chart_generator.create_radar_chart(scores, df)
            
        if fig:
            st.pyplot(fig)
    
    with col2:
        # Email section
        st.markdown("### Results Management")
        email = st.text_input(
            "Email address",
            key="export_email",
            placeholder="Press enter to check previous results",
            on_change=handle_email_change
        )
        
        if email:
            if not st.session_state.get('email_valid', False):
                st.error("Please enter a valid email address")
            else:
                # Consent checkboxes
                data_sharing = st.checkbox(
                    "Share my results and receive a copy by email",
                    value=st.session_state.get('data_sharing', False),
                    key="data_sharing"
                )
                
                mailing_list = st.checkbox(
                    "Subscribe to our mailing list for future updates",
                    value=st.session_state.get('mailing_list', False),
                    key="mailing_list"
                )
                
                # Apply button with help text
                if st.button(
                    "Apply Choices",
                    help="Update your preferences for data storage and mailing list"
                ):
                    handle_preferences_update(email, mailing_list, data_sharing, scores)
        
        # Download options (always available)
        st.markdown("### Download Results")
        csv_data = generate_csv_data(df, st.session_state.responses)
        st.download_button(
            "Download as CSV",
            data=csv_data,
            file_name="assessment_results.csv",
            mime="text/csv",
            help="Download your results in CSV format"
        )

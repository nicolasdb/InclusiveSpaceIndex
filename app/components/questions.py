"""
Questions component for displaying and handling question interactions.
"""
import logging
import streamlit as st
from utils.styles import apply_style
from utils.state import (
    get_current_response, 
    update_response, 
    set_total_questions,
    get_completion_status
)

# Configure logging
logger = logging.getLogger(__name__)

def display_question(row, idx):
    """
    Display a single question with radio buttons.
    
    Args:
        row: DataFrame row containing question data
        idx: Question index
    """
    # Question container with number
    st.markdown(
        f'<div class="{apply_style("question")}">Q{idx + 1}: {row["question"]}</div>',
        unsafe_allow_html=True
    )
    
    # Options without point values
    options = [
        row['option1'],
        row['option2'],
        row['option3'],
        row['option4'],
        row['option5']
    ]
    
    # Get current value from session state
    current_value = get_current_response(idx)
    
    # Radio button with callback
    _ = st.radio(
        "Choose:",
        options=range(len(options)),
        format_func=lambda x: options[x],
        key=f"q_{idx}",
        horizontal=True,
        label_visibility="collapsed",
        on_change=update_response,
        args=(idx,),
        index=current_value
    )

def display_sections(df):
    """
    Display all sections as tabs with their questions.
    
    Args:
        df: DataFrame containing questions data
    """
    # Update total questions count
    total_questions = len(df)
    set_total_questions(total_questions)
    
    # Get unique sections
    sections = df['section'].unique()
    logger.debug(f"Creating tabs for sections: {sections}")
    
    # Create tabs for each section
    tabs = st.tabs([f"📚 {section}" for section in sections])
    
    # Display questions for each section in its tab
    for section, tab in zip(sections, tabs):
        with tab:
            section_questions = df[df['section'] == section]
            logger.debug(f"Displaying {len(section_questions)} questions for section: {section}")
            
            for idx, row in section_questions.iterrows():
                display_question(row, idx)
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing between questions

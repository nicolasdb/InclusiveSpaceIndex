"""
Session state management for the maturity assessment.
"""
import logging
import streamlit as st
from .scoring import calculate_scores

# Configure logging
logger = logging.getLogger(__name__)

def init_session_state():
    """Initialize all session state variables."""
    if 'responses' not in st.session_state:
        logger.debug("Initializing responses with default values")
        # Initialize all questions with default response (0)
        st.session_state.responses = {str(i): 0 for i in range(25)}  # 25 total questions
        st.session_state.scores_need_update = True
        st.session_state.current_scores = None
        st.session_state.completed_questions = set()  # Track explicitly answered questions
        st.session_state.total_questions = 25

def update_response(idx):
    """
    Update response and trigger score recalculation.
    
    Args:
        idx: Question index
    """
    key = f"q_{idx}"
    if key in st.session_state:
        logger.debug(f"Updating response for question {idx}")
        st.session_state.responses[str(idx)] = st.session_state[key]
        st.session_state.completed_questions.add(str(idx))
        st.session_state.scores_need_update = True

def reset_responses():
    """Reset all responses to default values and clear scores."""
    logger.debug("Resetting responses to defaults")
    st.session_state.responses = {str(i): 0 for i in range(25)}  # Reset to default (0)
    st.session_state.completed_questions = set()
    st.session_state.scores_need_update = True
    st.session_state.current_scores = None

def update_scores(df):
    """
    Update scores if needed.
    
    Args:
        df: DataFrame containing questions data
        
    Returns:
        dict containing current scores
    """
    if st.session_state.scores_need_update or st.session_state.current_scores is None:
        logger.debug("Recalculating scores")
        st.session_state.current_scores = calculate_scores(df)
        st.session_state.scores_need_update = False
    
    return st.session_state.current_scores

def get_current_response(idx):
    """
    Get current response for a question.
    
    Args:
        idx: Question index
        
    Returns:
        int: Current response index (0-4)
    """
    return st.session_state.responses.get(str(idx), 0)

def set_total_questions(total):
    """
    Set the total number of questions.
    
    Args:
        total: Total number of questions
    """
    st.session_state.total_questions = total

def get_completion_status():
    """
    Get the current completion status.
    
    Returns:
        tuple: (completed_count, total_questions, completion_percentage)
    """
    completed = len(st.session_state.completed_questions)
    total = st.session_state.total_questions
    percentage = (completed / total * 100) if total > 0 else 0
    return completed, total, percentage

def is_assessment_complete():
    """
    Check if assessment can be submitted.
    Always returns True since we allow submission with default values.
    
    Returns:
        bool: Always True, as we allow submission at any time
    """
    return True

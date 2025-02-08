"""
Scoring system and calculations for the maturity assessment.
"""
import logging
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)

# Scoring system with exponential progression
OPTION_SCORES = {
    0: 0,   # Not implemented
    1: 1,   # Initial steps
    2: 2,   # Partial
    3: 4,   # Mostly
    4: 8    # Fully
}

# Constants
MAX_POINTS_PER_QUESTION = 8  # Maximum points possible per question
TOTAL_QUESTIONS = 25         # Total number of questions
MAX_POSSIBLE_SCORE = MAX_POINTS_PER_QUESTION * TOTAL_QUESTIONS  # 200 points

def calculate_scores(df):
    """
    Calculate scores for all sections.
    
    Args:
        df: DataFrame containing questions data
        
    Returns:
        dict containing:
            - total_score: int
            - total_max: int
            - section_scores: dict of section names to scores
    """
    total_score = 0
    total_max = 0
    section_scores = {}
    
    logger.debug("Calculating scores for all sections")
    
    for section in df['section'].unique():
        section_qs = df[df['section'] == section]
        section_max = len(section_qs) * MAX_POINTS_PER_QUESTION
        section_score = sum(
            OPTION_SCORES.get(st.session_state.responses.get(str(idx), 0), 0)
            for idx in section_qs.index
        )
        section_scores[section] = section_score
        total_score += section_score
        total_max += section_max
        
        logger.debug(f"Section '{section}' score: {section_score}/{section_max}")
    
    logger.debug(f"Total score: {total_score}/{total_max}")
    
    return {
        'total_score': total_score,
        'total_max': total_max,
        'section_scores': section_scores
    }

def get_section_score(df, section):
    """
    Calculate score for a specific section.
    
    Args:
        df: DataFrame containing questions data
        section: Name of the section to calculate score for
        
    Returns:
        tuple of (score, max_possible)
    """
    section_qs = df[df['section'] == section]
    section_max = len(section_qs) * MAX_POINTS_PER_QUESTION
    section_score = sum(
        OPTION_SCORES.get(st.session_state.responses.get(str(idx), 0), 0)
        for idx in section_qs.index
    )
    
    return section_score, section_max

def get_question_score(idx):
    """
    Get score for a specific question.
    
    Args:
        idx: Question index
        
    Returns:
        tuple of (score, max_possible)
    """
    response = st.session_state.responses.get(str(idx), 0)
    score = OPTION_SCORES.get(response, 0)
    return score, MAX_POINTS_PER_QUESTION

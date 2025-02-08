"""
Calculator module for computing scores in the evaluation system.
"""
from .scoring import (
    OPTION_SCORES,
    MAX_POINTS_PER_QUESTION,
    TOTAL_QUESTIONS,
    MAX_POSSIBLE_SCORE
)

def calculate_section_score(responses: dict, questions_df, section: str) -> tuple[int, int]:
    """
    Calculate the score for a specific section.
    
    Args:
        responses: Dictionary of question indices and their selected option indices
        questions_df: DataFrame containing questions data
        section: Section name to calculate score for
        
    Returns:
        Tuple of (score, max_possible_score) for the section
    """
    section_questions = questions_df[questions_df['section'].astype(str).str.strip() == str(section).strip()]
    section_score = 0
    max_possible = len(section_questions) * MAX_POINTS_PER_QUESTION
    
    for idx in section_questions.index:
        if str(idx) in responses:
            section_score += OPTION_SCORES.get(responses[str(idx)], 0)
            
    return section_score, max_possible

def calculate_total_score(responses: dict, questions_df) -> tuple[dict, int, int]:
    """
    Calculate scores for all sections and total.
    
    Args:
        responses: Dictionary of question indices and their selected option indices
        questions_df: DataFrame containing questions data
        
    Returns:
        Tuple of (section_scores, total_score, max_possible_score)
        where section_scores is a dictionary of section names to (score, max) tuples
    """
    sections = questions_df['section'].unique()
    section_scores = {}
    total_score = 0
    total_max = 0
    
    for section in sections:
        score, max_score = calculate_section_score(responses, questions_df, section)
        section_scores[section] = (score, max_score)
        total_score += score
        total_max += max_score
        
    return section_scores, total_score, total_max

"""
CSS styles and theme management for the maturity assessment.
"""
import streamlit as st

def inject_custom_css():
    """
    Inject custom CSS with theme-aware styling.
    """
    st.markdown("""
        <style>
        /* Question styling */
        .question-text {
            color: var(--text-color);
            background: var(--background-color);
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--primary-color);
            margin: 1rem 0;
            font-size: 1.2rem;
            font-weight: bold; /* Set text to bold */
        }
        
        /* Radio options */
        .stRadio > label {
            color: var(--text-color) !important;
            background: var(--background-color);
            border: 1px solid var(--primary-color);
            padding: 0.5rem;
            border-radius: 0.5rem;
            min-width: 150px;
            text-align: center;
        }
        /* Theme-aware radio backgrounds */
        [data-theme="light"] .stRadio > label {
            background: rgba(0, 0, 0, 0.05);
        }
        
        [data-theme="dark"] .stRadio > label {
            background: rgba(255, 255, 255, 0.1);
        }
        
        /* Style radio labels */
        .stRadio [data-testid="stMarkdownContainer"] {
            margin-bottom: 0.5rem;
        }
        
        /* Progress bars */
        .stProgress > div > div > div {
            background-color: var(--primary-color);
        }
        
        /* Section divider */
        hr {
            margin: 2rem 0;
            border-color: var(--primary-color);
        }
        
        /* Metric styling */
        .metric-container {
            background: var(--background-color);
            border: 1px solid var(--primary-color);
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .section-header {
            color: var(--text-color);
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 0.5rem;
            margin: 1.5rem 0;
        }
        
        /* Score display */
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--text-color);
            text-align: center;
            padding: 1rem;
            background: var(--
            border-radius: 0.5rem;
            border: 2px solid var(--primary-color);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_style(element_type: str) -> str:
    """
    Get the appropriate class name for styling different elements.
    
    Args:
        element_type: Type of element to style (e.g., 'question', 'section', etc.)
        
    Returns:
        str: CSS class name for the element
    """
    style_map = {
        'question': 'question-text',
        'section': 'section-header',
        'metric': 'metric-container',
        'score': 'score-display'
    }
    return style_map.get(element_type, '')

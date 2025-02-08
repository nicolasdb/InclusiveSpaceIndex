"""
Data loader module for handling questions data from CSV or Supabase.
"""
import os
import logging
import pandas as pd
from supabase import create_client

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_supabase_client():
    """Initialize and return Supabase client."""
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    return create_client(url, key)

def load_questions_from_csv(file_path: str = "/data/questions.csv") -> pd.DataFrame:
    """
    Load questions from CSV file.
    
    Args:
        file_path: Path to the CSV file, defaults to container's data directory
        
    Returns:
        DataFrame containing questions data
    """
    try:
        # Debug file path
        logger.debug(f"Attempting to load CSV from: {file_path}")
        logger.debug(f"Current working directory: {os.getcwd()}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Questions file not found at: {file_path}")
            
        # Load CSV with explicit encoding
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Debug DataFrame info
        logger.debug(f"DataFrame shape: {df.shape}")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
        
        # Validate DataFrame structure
        required_columns = ['section', 'question', 'option1', 'option2', 
                          'option3', 'option4', 'option5']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing columns in CSV: {missing_columns}")
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        logger.info("Successfully loaded questions from CSV")
        return df
        
    except Exception as e:
        # Add context to the error
        error_msg = (f"Error loading questions from CSV: {str(e)}\n"
                    f"Current working directory: {os.getcwd()}\n"
                    f"File path: {file_path}")
        logger.error(error_msg)
        raise Exception(error_msg)

def load_questions_from_supabase() -> pd.DataFrame:
    """
    Load questions from Supabase table.
    
    Returns:
        DataFrame containing questions data
    """
    try:
        supabase = get_supabase_client()
        context_id = os.getenv("CONTEXT_ID", "")
        table_name = os.getenv("QUESTIONS_TABLE", "maturity_questions")
        
        response = supabase.table(table_name)\
            .select("*")\
            .eq("context_id", context_id)\
            .execute()
            
        if response.data:
            return pd.DataFrame(response.data)
        else:
            raise Exception("No questions found in Supabase")
            
    except Exception as e:
        raise Exception(f"Error loading questions from Supabase: {str(e)}")

def load_questions() -> pd.DataFrame:
    """
    Load questions from configured source (CSV by default).
    
    Returns:
        DataFrame containing questions data
    """
    source = os.getenv("QUESTIONS_SOURCE", "csv").lower()
    
    if source == "supabase":
        return load_questions_from_supabase()
    else:
        return load_questions_from_csv()

def save_result(email: str, responses: dict, section_scores: dict, 
                total_score: int, total_max: int) -> bool:
    """
    Save evaluation results to Supabase.
    
    Args:
        email: User's email
        responses: Dictionary of responses
        section_scores: Dictionary of section scores
        total_score: Total score achieved
        total_max: Maximum possible score
        
    Returns:
        bool indicating success
    """
    try:
        supabase = get_supabase_client()
        context_id = os.getenv("CONTEXT_ID", "")
        
        data = {
            "context_id": context_id,
            "email": email,
            "responses": responses,
            "section_scores": section_scores,
            "total_score": total_score,
            "total_max": total_max
        }
        
        response = supabase.table("results").insert(data).execute()
        return bool(response.data)
        
    except Exception as e:
        raise Exception(f"Error saving results: {str(e)}")

def save_to_mailing_list(email: str) -> bool:
    """
    Add user to mailing list if they opted in.
    
    Args:
        email: User's email
        
    Returns:
        bool indicating success
    """
    try:
        supabase = get_supabase_client()
        context_id = os.getenv("CONTEXT_ID", "")
        
        data = {
            "email": email,
            "context_id": context_id
        }
        
        response = supabase.table("mailing_list").insert(data).execute()
        return bool(response.data)
        
    except Exception as e:
        # Ignore duplicate email errors
        if "duplicate key" in str(e).lower():
            return True
        raise Exception(f"Error adding to mailing list: {str(e)}")

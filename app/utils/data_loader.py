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

def load_questions_from_csv(file_path: str = None) -> pd.DataFrame:
    """
    Load questions from CSV file.
    
    Args:
        file_path: Path to the CSV file, defaults to container's data directory
        
    Returns:
        DataFrame containing questions data
    """
    try:
        # Get file path from environment variable or use provided path
        env_path = os.getenv("QUESTIONS_FILE", "/data/questions.csv")
        file_path = file_path or env_path

        # Try multiple possible file paths
        possible_paths = [
            file_path,  # Try environment variable path or provided path first
            "data/questions.csv",  # Relative to project root
            "../data/questions.csv",  # One level up (from app dir)
            "../../data/questions.csv",  # Two levels up
        ]
        
        # Debug paths being tried
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Attempting to load CSV from these paths: {possible_paths}")
        
        # Try each path
        for try_path in possible_paths:
            logger.debug(f"Trying path: {try_path}")
            if os.path.exists(try_path):
                logger.info(f"Found questions file at: {try_path}")
                df = pd.read_csv(try_path, encoding='utf-8')
                break
        else:
            # If no file is found, raise error with all attempted paths
            error_msg = f"Questions file not found in any of these locations: {possible_paths}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
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

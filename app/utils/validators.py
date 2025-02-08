"""Input validation utilities."""

import re
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

# Email validation regex pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email:
        return False
    return bool(re.match(EMAIL_PATTERN, email))

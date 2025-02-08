"""Supabase client and database operations."""

import os
import logging
from typing import Dict, Any, Optional
from supabase import create_client, Client

# Configure logging
logger = logging.getLogger(__name__)

class SupabaseManager:
    """Manages Supabase database operations."""
    
    def __init__(self):
        """Initialize Supabase client."""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key) if self.url and self.key else None
        
    def check_previous_results(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Check if previous results exist for the given email.
        
        Args:
            email: Email address to check
            
        Returns:
            Optional[Dict]: Previous results if found, None otherwise
        """
        try:
            if not self.client:
                logger.error("Supabase client not initialized")
                return None
                
            response = self.client.table("assessment_results").select("*").eq("email", email).execute()
            if response.data:
                # Return the most recent result if multiple exist
                return response.data[-1]
            return None
            
        except Exception as e:
            logger.error(f"Error checking previous results: {str(e)}")
            return None
            
    def get_user_preferences(self, email: str) -> Dict[str, bool]:
        """
        Get user's consent preferences based on presence in tables.
        
        Args:
            email: Email address to check
            
        Returns:
            Dict with mailing_list and data_sharing preferences
        """
        try:
            if not self.client:
                return {"mailing_list": False, "data_sharing": False}
            
            # Check if email exists in each table
            results_response = self.client.table("assessment_results").select("id").eq("email", email).execute()
            mailing_response = self.client.table("assessment_mailing_list").select("id").eq("email", email).execute()
            
            return {
                "mailing_list": len(mailing_response.data) > 0,
                "data_sharing": len(results_response.data) > 0
            }
            
        except Exception as e:
            logger.error(f"Error getting user preferences: {str(e)}")
            return {"mailing_list": False, "data_sharing": False}
            
    def update_preferences(self, email: str, mailing_list: bool, data_sharing: bool) -> bool:
        """
        Update user's consent preferences.
        
        Args:
            email: User's email address
            mailing_list: Whether to subscribe to mailing list
            data_sharing: Whether to store and share results
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            if not self.client:
                return False
            
            # Handle mailing list preference
            if mailing_list:
                self.client.table("assessment_mailing_list").upsert({"email": email}).execute()
            else:
                self.client.table("assessment_mailing_list").delete().eq("email", email).execute()
            
            # Handle data sharing preference
            if not data_sharing:
                self.client.table("assessment_results").delete().eq("email", email).execute()
                
            return True
            
        except Exception as e:
            logger.error(f"Error updating preferences: {str(e)}")
            return False
            
    def store_results(self, email: str, responses: Dict[str, int], total_score: int, total_max: int) -> bool:
        """
        Store assessment results.
        
        Args:
            email: User's email address
            responses: Dictionary of question indices and selected options
            total_score: Total score achieved
            total_max: Maximum possible score
            
        Returns:
            bool: True if storage successful, False otherwise
        """
        try:
            if not self.client:
                return False
                
            data = {
                "email": email,
                "responses": responses,
                "total_score": total_score,
                "total_max": total_max
            }
            
            # Store new results
            self.client.table("assessment_results").insert(data).execute()
            return True
            
        except Exception as e:
            logger.error(f"Error storing results: {str(e)}")
            return False

# Create a singleton instance
supabase = SupabaseManager()

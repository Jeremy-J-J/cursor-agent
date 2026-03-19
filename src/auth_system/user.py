"""
User class with get_user method implementation
"""

from .models import CustomUser
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class User:
    """
    A class representing a user with methods for user operations
    """
    
    def __init__(self, user_id: int = None, username: str = None):
        """
        Initialize a User instance
        
        Args:
            user_id (int): The ID of the user
            username (str): The username of the user
        """
        self.user_id = user_id
        self.username = username
    
    def get_user(self, user_id: int) -> Optional[CustomUser]:
        """
        Retrieve a user by ID from the database
        
        Args:
            user_id (int): The ID of the user to retrieve
            
        Returns:
            CustomUser: The user object if found, None otherwise
            
        Raises:
            Exception: If there's a database error during retrieval
        """
        try:
            # Validate input
            if not isinstance(user_id, int) or user_id <= 0:
                logger.warning(f"Invalid user_id provided: {user_id}")
                return None
            
            # Attempt to retrieve the user from the database
            user = CustomUser.objects.get(id=user_id)
            logger.debug(f"Successfully retrieved user with ID: {user_id}")
            return user
            
        except CustomUser.DoesNotExist:
            # User with this ID doesn't exist
            logger.info(f"User with ID {user_id} not found")
            return None
        except Exception as e:
            # Handle any other database-related errors
            logger.error(f"Database error while retrieving user {user_id}: {str(e)}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[CustomUser]:
        """
        Retrieve a user by email from the database
        
        Args:
            email (str): The email of the user to retrieve
            
        Returns:
            CustomUser: The user object if found, None otherwise
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Database error while retrieving user by email {email}: {str(e)}")
            return None
    
    def get_all_users(self) -> list:
        """
        Retrieve all users from the database
        
        Returns:
            list: A list of all user objects
        """
        try:
            return list(CustomUser.objects.all())
        except Exception as e:
            logger.error(f"Database error while retrieving all users: {str(e)}")
            return []
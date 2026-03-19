"""
User Manager for handling user-related operations
"""
from .models import CustomUser


class UserManager:
    """
    A class to manage user operations
    """
    
    def get_user(self, user_id):
        """
        Retrieve a user by ID
        
        Args:
            user_id (int): The ID of the user to retrieve
            
        Returns:
            CustomUser: The user object if found, None otherwise
        """
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    
    def get_user_by_email(self, email):
        """
        Retrieve a user by email
        
        Args:
            email (str): The email of the user to retrieve
            
        Returns:
            CustomUser: The user object if found, None otherwise
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
    
    def get_all_users(self):
        """
        Retrieve all users
        
        Returns:
            QuerySet: A queryset of all users
        """
        return CustomUser.objects.all()
    
    def get_users_by_role(self, role):
        """
        Retrieve users by role
        
        Args:
            role (str): The role to filter users by
            
        Returns:
            QuerySet: A queryset of users with the specified role
        """
        return CustomUser.objects.filter(role=role)
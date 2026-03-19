"""
Example usage of UserManager class
"""
from src.auth_system.user_manager import UserManager
from django.contrib.auth import get_user_model

# Initialize the UserManager
user_manager = UserManager()

# Get a user by ID
user = user_manager.get_user(1)
if user:
    print(f"Found user: {user.email}")
else:
    print("User not found")

# Get a user by email
user = user_manager.get_user_by_email("test@example.com")
if user:
    print(f"Found user by email: {user.email}")
else:
    print("User not found")

# Get all users
all_users = user_manager.get_all_users()
print(f"Total users: {all_users.count()}")

# Get users by role
admin_users = user_manager.get_users_by_role("admin")
print(f"Admin users: {admin_users.count()}")
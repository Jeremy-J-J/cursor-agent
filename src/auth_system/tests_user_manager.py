"""
Tests for UserManager class
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from src.auth_system.user_manager import UserManager

CustomUser = get_user_model()


class UserManagerTestCase(TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        # Create test users
        self.user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            role='user'
        )
        self.user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            role='admin'
        )
        self.user3 = CustomUser.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='testpass123',
            role='premium'
        )

    def test_get_user_exists(self):
        """Test getting an existing user by ID"""
        user = self.user_manager.get_user(self.user1.id)
        self.assertEqual(user, self.user1)

    def test_get_user_not_exists(self):
        """Test getting a non-existing user by ID"""
        user = self.user_manager.get_user(999)
        self.assertIsNone(user)

    def test_get_user_by_email_exists(self):
        """Test getting an existing user by email"""
        user = self.user_manager.get_user_by_email('test1@example.com')
        self.assertEqual(user, self.user1)

    def test_get_user_by_email_not_exists(self):
        """Test getting a non-existing user by email"""
        user = self.user_manager.get_user_by_email('nonexistent@example.com')
        self.assertIsNone(user)

    def test_get_all_users(self):
        """Test getting all users"""
        users = self.user_manager.get_all_users()
        self.assertEqual(users.count(), 3)

    def test_get_users_by_role(self):
        """Test getting users by role"""
        users = self.user_manager.get_users_by_role('user')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.user1)

        users = self.user_manager.get_users_by_role('admin')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.user2)
"""
Edge case tests for the get_user function specifically
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from src.auth_system.user_manager import UserManager
from src.auth_system.models import CustomUser

User = get_user_model()


class GetUserEdgeCasesTestCase(TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            role='user'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            role='admin'
        )
        
    def test_get_user_with_none_id(self):
        """Test get_user with None ID"""
        user = self.user_manager.get_user(None)
        self.assertIsNone(user)
        
    def test_get_user_with_empty_string_id(self):
        """Test get_user with empty string ID"""
        user = self.user_manager.get_user("")
        self.assertIsNone(user)
        
    def test_get_user_with_large_id(self):
        """Test get_user with very large ID"""
        user = self.user_manager.get_user(999999999999999999999)
        self.assertIsNone(user)
        
    def test_get_user_with_negative_id(self):
        """Test get_user with negative ID"""
        user = self.user_manager.get_user(-1)
        self.assertIsNone(user)
        
    def test_get_user_with_float_id(self):
        """Test get_user with float ID"""
        user = self.user_manager.get_user(1.5)
        self.assertIsNone(user)
        
    def test_get_user_with_boolean_id(self):
        """Test get_user with boolean ID"""
        user = self.user_manager.get_user(True)
        self.assertIsNone(user)
        
    def test_get_user_with_list_id(self):
        """Test get_user with list ID"""
        user = self.user_manager.get_user([1])
        self.assertIsNone(user)
        
    def test_get_user_with_dict_id(self):
        """Test get_user with dict ID"""
        user = self.user_manager.get_user({'id': 1})
        self.assertIsNone(user)
        
    def test_get_user_with_zero_id(self):
        """Test get_user with zero ID"""
        user = self.user_manager.get_user(0)
        self.assertIsNone(user)
        
    def test_get_user_with_valid_ids(self):
        """Test get_user with valid IDs"""
        user = self.user_manager.get_user(self.user1.id)
        self.assertEqual(user, self.user1)
        
        user = self.user_manager.get_user(self.user2.id)
        self.assertEqual(user, self.user2)
        
    def test_get_user_by_email_with_empty_string(self):
        """Test get_user_by_email with empty string"""
        user = self.user_manager.get_user_by_email("")
        self.assertIsNone(user)
        
    def test_get_user_by_email_with_none(self):
        """Test get_user_by_email with None"""
        user = self.user_manager.get_user_by_email(None)
        self.assertIsNone(user)
        
    def test_get_user_by_email_with_invalid_format(self):
        """Test get_user_by_email with invalid email format"""
        user = self.user_manager.get_user_by_email("invalid-email")
        self.assertIsNone(user)
        
    def test_get_user_by_email_with_special_characters(self):
        """Test get_user_by_email with special characters"""
        user = self.user_manager.get_user_by_email("test+tag@example.com")
        self.assertIsNone(user)  # This should not exist
        
        # Create a user with special characters
        special_user = User.objects.create_user(
            username='specialuser',
            email='test+tag@example.com',
            password='testpass123',
            role='user'
        )
        
        user = self.user_manager.get_user_by_email("test+tag@example.com")
        self.assertEqual(user, special_user)
        
    def test_get_user_by_email_case_sensitivity(self):
        """Test get_user_by_email case sensitivity"""
        # Create a user with lowercase email
        user = User.objects.create_user(
            username='caseuser',
            email='case@example.com',
            password='testpass123',
            role='user'
        )
        
        # Test with lowercase (should find)
        found_user = self.user_manager.get_user_by_email('case@example.com')
        self.assertEqual(found_user, user)
        
        # Test with uppercase (should not find due to case sensitivity)
        found_user = self.user_manager.get_user_by_email('CASE@EXAMPLE.COM')
        self.assertIsNone(found_user)
        
    def test_get_user_by_email_with_whitespace(self):
        """Test get_user_by_email with whitespace"""
        user = self.user_manager.get_user_by_email(" test@example.com ")
        self.assertIsNone(user)
        
    def test_get_user_by_email_with_unicode(self):
        """Test get_user_by_email with unicode characters"""
        # Create a user with unicode in email
        unicode_user = User.objects.create_user(
            username='unicodeuser',
            email='test@exämple.com',
            password='testpass123',
            role='user'
        )
        
        user = self.user_manager.get_user_by_email('test@exämple.com')
        self.assertEqual(user, unicode_user)
        
    def test_get_user_performance_with_many_users(self):
        """Test get_user performance with many users (basic test)"""
        # Create multiple users
        for i in range(100):
            User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass123',
                role='user'
            )
            
        # Test getting a user by ID
        user = self.user_manager.get_user(self.user1.id)
        self.assertEqual(user, self.user1)
        
    def test_get_user_with_deleted_user(self):
        """Test get_user with deleted user"""
        # Delete a user
        user_to_delete = User.objects.create_user(
            username='deleteuser',
            email='delete@example.com',
            password='testpass123',
            role='user'
        )
        
        user_id = user_to_delete.id
        user_to_delete.delete()
        
        # Try to get the deleted user
        user = self.user_manager.get_user(user_id)
        self.assertIsNone(user)
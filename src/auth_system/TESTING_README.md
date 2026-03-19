# Authentication System Test Suite

This comprehensive test suite covers all aspects of the user authentication system, including edge cases for the `get_user` function and all authentication flows.

## Test Coverage

### 1. User Manager Tests
- `get_user` function with valid and invalid IDs
- `get_user_by_email` function with valid and invalid emails
- `get_all_users` function
- `get_users_by_role` function

### 2. Authentication Flow Tests
- User registration
- User login (success and failure cases)
- Password reset functionality
- Email verification
- User profile management
- Role-based access control
- Token-based authentication

### 3. Edge Case Tests
- Invalid ID types (None, empty string, negative numbers, floats, etc.)
- Invalid email formats
- Case sensitivity in email lookups
- Expired tokens handling
- Account lockout scenarios
- Unicode and special character handling

## Running Tests

To run all tests:

```bash
cd src/auth_system
python manage.py test
```

To run specific test files:

```bash
python manage.py test tests_auth.py
python manage.py test tests_get_user_edge_cases.py
python manage.py test tests_user_manager.py
```

## Test Structure

The test suite is organized into multiple files:
- `tests.py` - Basic authentication tests
- `tests_auth.py` - Comprehensive authentication flow tests
- `tests_get_user_edge_cases.py` - Edge case tests for get_user function
- `tests_user_manager.py` - User manager specific tests

Each test follows the AAA pattern (Arrange, Act, Assert) and includes proper setup and teardown.
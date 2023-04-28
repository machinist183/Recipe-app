"""
    Tests to check the functionality of custom autn User model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    def test_user_creation_on_email_password_success(self):
        '''
            tests if user is created after providing email and password
        '''
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password(password))
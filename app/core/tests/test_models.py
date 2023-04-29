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

    def test_user_email_normalization(self):
        """
        Test to check is the email address is normalised
        """
        email_list = [
            ('test@Example.com' ,'test@example.com'),
            ('Test@EXAMPLE.COM','Test@example.com')
        ]

        for email , expect_email  in email_list:
            user  = get_user_model().objects.create_user(
                email = email
            )
            self.assertEqual(user.email , expect_email)

    def test_user_no_email_raises_value_error(self):
        """
        test to validate raising error when no email is provided
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('')
    
    def test_user_check_superuser_created(self):
        """
        Test to check is the superuser is created
        """
        email = 'test@example.com'
        password = 'testpass123'
        user  = get_user_model().objects.create_superuser(
                email = email,
                password = password
                )
        self.assertEqual(user.email , email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
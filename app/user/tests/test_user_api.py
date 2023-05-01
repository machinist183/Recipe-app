"""
Tests to check the functionality of User Api 
"""
from django.contrib.auth import get_user_model
from django.urls  import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient 

CREATE_USER_URL =  reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(params):
    '''Create a new user'''
    return get_user_model().objects.create_user(**params)

class PublicTestForUserAPI(APITestCase):
    '''
    Test the functionalities of user api which doesnt require authentication
    '''
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'first_name':'test user',
            'last_name':'test'
        }

    def test_create_user_success(self):

        '''Test the successfull creation of User'''
        print(self.payload)
        res = self.client.post(CREATE_USER_URL ,self.payload)
        print(res.data)
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = self.payload['email'])

        self.assertTrue(user.check_password(self.payload['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # self.assertNotIn('password' , res.data)

    def test_user_email_already_exist(self):

        '''Tests to not allow duplicate emails'''

        create_user(self.payload)
        res = self.client.post(CREATE_USER_URL , self.payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):

        '''Test to throw error when provided password is too short'''

        self.payload['password'] = 'test'
        res = self.client.post(CREATE_USER_URL , self.payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)

    def test_generate_token_for_valid_credentials(self):

        '''Test to ensure valid credentials creates token''' 

        login_credentials = {
            'email' : self.payload['email'],
            'password':self.payload['password']
        }
        create_user(self.payload)
        res = self.client.post(TOKEN_URL , login_credentials)

        self.assertTrue(res.status_code , status.HTTP_200_OK)
        self.assertIn('token', res.data)


    def test_check_no_token_for_empty_pass(self):

        '''Test to ensure empty password field doenst generate token'''
        
        login_credentials = {
            'email' : self.payload['email'],
            'password':''
        }
        create_user(self.payload)
        res = self.client.post(TOKEN_URL , login_credentials)

        self.assertTrue(res.status_code , status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)


    def test_no_token_for_bad_cred(self):

        '''Test  to ensure wrong credential doesnt geneerate a token'''

        create_user(self.payload)
        login_credentials = {
            'email' : self.payload['email'],
            'password':'badpass123'
        }
        res = self.client.post(TOKEN_URL , login_credentials)

        self.assertTrue(res.status_code , status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_me_access_declined_unauthorised(self):

        '''Test to check the get request for users/me/ endpoint is declined 
            for unauthorised user'''
        
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(APITestCase):

    '''Tests to check all the '''

    def setUp(self):

        self.user = create_user({
            'email':'test@example.com',
            'password':'testpass',
            'first_name':'test',
            'last_name':'user'
        })

        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_retriew_profile_success(self):

        '''Test to check if authenticated user can successfully login'''

        res = self.client.get(ME_URL)
        
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data ,{
            'email':'test@example.com',
            'first_name':'test',
            'last_name':'user'
        })

    def test_post_method_not_allowed_for_me(self):

        '''Test to check post method is not allowed for user/me'''

        res = self.client.post(ME_URL , {})
        self.assertEqual(res.status_code , status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_modify_user_details(self):

        '''Test to check user update using patch method'''

        payload = {
            'first_name':'new first name',
            'last_name':'new last name',
            'password':'newpass123'
        }
        res = self.client.patch(ME_URL , payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(self.user.first_name , payload['first_name'])
        self.assertEqual(self.user.last_name , payload['last_name'])
        self.assertTrue(self.user.check_password(payload['password']))

        


from django.test import TestCase
from rest_framework.test import APIClient
from ninja import NinjaAPI
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your tests here.
class AccountsTests(TestCase):
    def setUp(self):
        self.client=APIClient()
    def test_signup(self):
        data={
            'username':'testuser',
            'password':'password123',
            'name':'Test User',
            'email':'test@email.com',
            'phone':'1234567890'
        }
        response=self.client.post('/accounts/signup',data,format='json')
        self.assertEqual(response.status_code,200)
        self.assertIn('message',response.json())
        print(response.json())
        user = User.objects.get(username="testuser")
        profile = Profile.objects.get(user=user)
        print(profile)
        print("###############################signup done")
        data = {
            'username': 'testuser',
            'password': 'password123'

        }
        response = self.client.post('/accounts/login', data, format='json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        print(response_data)
        print("##############################loginDone")
        check_response=self.client.get('/accounts/profile',format='json')
        print(check_response.json())
        logout_response = self.client.post('/accounts/logout', format='json')
        print(logout_response.json())
    # def test_login(self):
    #     data={
    #         'username':'testuser',
    #         'password':'password123'
    #
    #     }
    #     response=self.client.post('/accounts/login',data,format='json')
    #     self.assertEqual(response.status_code,200)
    #     response_data=response.json()
    #     print(response_data)
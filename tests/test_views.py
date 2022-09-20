from accounts.views import login_view
from django.test import TestCase,Client
from  banking.models import *
from django.urls import reverse,resolve

class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()
        self.customer_account_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "rik@gmail.com",
            "password": "1245678",
            # 'password2': "1245678"
        }


        self.login_payload = {
            "email": "rik@gmail.com",
            "password": "1245678"
        }

class Register_Test(TestUrls):

    def test_register_url(self):
        response = self.client.post(reverse('register'), self.customer_account_payload)
        self.assertEqual(response.status_code, 200)


    def login_url(self):
        response = self.client.post(reverse('login'), self.login_payload)
        self.assertEqual(response.status_code, 200)

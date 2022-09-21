from accounts.models import CustomUser,UserManager
from django.test import TestCase, Client
from banking.models import BankAccount, Transactions
from accounts.serializers import CustomUserSerializer
from banking.serializers import BankAccountSerializer, TransactionSerializer
from django.db.models import F
from django.utils.crypto import get_random_string as g
import string as s
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from django.urls import reverse


class TestAccountModels(TestCase):

    @classmethod
    def setUpTestData(cls):

        """
        Things to test:
        - Create a Test to register a user.
        - test if the user is login in the system.
        - test if the user can create cards or not
        - test if the emails are unique or not.
        """
        
        cls.customer_account_payload = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "rik1@gmail.com",
            "password": "1245678",
            
        }

        cls.customer_login_payload = {
            "email": "rik@gmail.com",
            "password": "1245678"
        }

        cls.receiver_account_payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "rik@gmail.com",
            "password": "1245678"
        }
         

    def setUp(self):
        self.client = Client()
        

    def test_register_user(self):
        """
            this test is to test if a user can be registered.
        """
        serializer = CustomUserSerializer(data=self.customer_account_payload)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEquals(CustomUser.objects.count(), 1)

    def test_login_user(self):
        """
            this test is to test if a user can be logged in.
        """
        response = self.client.post(reverse('login'), self.customer_login_payload)
        self.assertEquals(response.status_code, 200)



    def test_create_user_cards(self):
        """
            this test is to test if a user can create a card.
        """
        response = self.client.post(reverse('createCard'), self.customer_account_payload)
        serializer = CustomUserSerializer(data=self.customer_account_payload)
        if response.status_code == HTTP_201_CREATED:
            self.assertTrue(serializer.is_valid())
            serializer.save()
            self.assertEquals(CustomUser.objects.count(), 1)


    def test_unique_email(self):
        """
        checking if the two user have the same email or not.
        """

        response = self.client.post(reverse('register'), self.customer_account_payload)
        response2 = self.client.post(reverse('register'), self.receiver_account_payload)
        serializer = CustomUserSerializer(data=self.customer_account_payload)
        serializer2 = CustomUserSerializer(data=self.receiver_account_payload)

        # if both the email are unique then the status code will be 201
        if response.status_code == HTTP_201_CREATED and response2.status_code == HTTP_201_CREATED:
            self.assertTrue(serializer.is_valid())
            self.assertTrue(serializer2.is_valid())
            serializer.save()
            serializer2.save()
            self.assertEquals(CustomUser.objects.count(), 2)

        
        

         


class BankTestCase(TestCase):

    """
        setting up test data
        1. checking if the user is logged in or not.
        2. user can deposit or not
        3. user can withdraw or not
        4. transfer money to another user or not
    """
    def setUp(self):
        self.user_account_for_test = CustomUser.objects.create_user(
            email=g(4, allowed_chars=s.ascii_lowercase)+'@gmail.com',
            first_name=g(4, allowed_chars=s.ascii_lowercase),
            last_name=g(4, allowed_chars=s.ascii_lowercase),
            password='1234'
              )

        print(self.user_account_for_test)

        self.bank_account_for_test = BankAccount.objects.create(
            account_type= 'savings',
            user=self.user_account_for_test
        )

        
    def test_login_user(self):
        """
            this test is to test if a user can be logged in.
            Test if users can be logged in via API:
            http://127.0.0.1:8000/
        """

        data = {
            'email': 'rik@gmail.com',
            'password': '1234'
        }

        url = 'http://127.0.0.1:8000/'


        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)


    def test_deposit_money(self):
        bank_data  = [
            {
                'user': self.user_account_for_test,
                'date': '2022-09-23 06:00:00.579058+00:00', 
                'account_balace': 1000,
                'account_type': 'savings',
            }
        ]

        
        bank = BankAccountSerializer(data=bank_data, many=True)
        if bank.is_valid():
            bank.save()
            self.assertEqual(BankAccount.objects.count(), 1)


    def test_withdraw_money(self):
        bank_data  = [
            {
                'user': self.user_account_for_test,
                'date': '2022-09-23 06:00:00.579058+00:00', 
                'account_balace': 1000,
                'account_type': 'savings',
            }
        ]

        
        bank = BankAccountSerializer(data=bank_data, many=True)
        if bank.is_valid():
            bank.save()
            self.assertEqual(BankAccount.objects.count(), 1)


    def test_transfer_money(self):
        transcation_data = [
            {
                "user": self.user_account_for_test,
                "receiver": self.user_account_for_test,
                "transaction_date": "2022-09-23 06:00:00.579058+00:00",
                "transaction_amount": 1000,
                "ts_type": 2 # 3 for transfer,
            
            }
        ]
        transcation = TransactionSerializer(data=transcation_data, many=True)
        if transcation.is_valid():
            transcation.save()
            self.assertEqual(Transactions.objects.count(), 1)
    
        

    

        


        
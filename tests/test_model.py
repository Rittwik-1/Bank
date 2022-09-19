from accounts.models import *
from django.test import TestCase, Client
from banking.models import *
from accounts.serializers import *
from banking.serializers import *


class TestAccountModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.customer_account_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "rik@gmail.com",
            "password": "1245678",
            
        }

        cls.receiver_account_payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@gmail.com",
            "password": "1245678"
        }
         

    def setUp(self):
        self.client = Client()
        
         
    def test_customer_create(self):

        serializer = CustomUserSerializer(data=self.customer_account_payload)
        self.client.post(reverse('register'), self.customer_account_payload)
        

        if self.client.post(reverse('register'), self.customer_account_payload).status_code == 200:

            self.assertTrue(serializer.is_valid())
            serializer.save()
            self.assertEquals(CustomUser.objects.count(), 1)
            


    def test_bank_account_create(self):
        global bank_account, bank, bank_other
        bank_account = {
            "user": CustomUser.objects.create_user(**self.customer_account_payload),
            "account_type": "savings",
            "account_balance": 10000
        }

        bank_account_receiver ={
            "user": CustomUser.objects.create_user(**self.receiver_account_payload),
            "account_type": "savings",
            "account_balance": 10001

        }

        bank = BankAccount.objects.create(**bank_account)
        bank_other = BankAccount.objects.create(**bank_account_receiver)
        self.assertEquals(BankAccount.objects.count(), 2)
        

    

        


     
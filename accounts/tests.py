
from django.test import TestCase
from .models import CustomUser
from banking.models import BankAccount
from django.utils.crypto import get_random_string as g
import string as s

class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(first_name='test', last_name='test', password = 'test')
        if CustomUser.objects.filter(
            first_name='test', last_name='test', password = 'test',
        ).exists():
            print('User Created')
        else:
            print('User Not Created')
    def test_user_created(self):
        self.assertEqual(CustomUser.objects.filter(
            first_name='test', last_name='test', password = 'test'
        ).exists(), True)


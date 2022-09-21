import pyexpat
import pytest
import sys
from accounts.models import CustomUser

from accounts.serializers import CustomUserSerializer
from banking.models import BankAccount
# @pytest.mark.skip(reason="not implemented yet") # this is a decorator which skips the test
# def test_example():
#     assert 1 == 1

# @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
# def test_example2():
#     assert 1 == 1



# @pytest.mark.xfail(reason="fails on purpose")
# def test_example3():
#     assert 1 == 1



# to run this
# pytest -m 'slow' # this will run all the tests with the slow marker
# @pytest.mark.slow
# def test_example4():
#     assert 1 == 1

# # A patter of writing tests
# # 1. Arrange
# # 2. Act 
# # 3. Assert 

# # fixtures are used to setup and teardown the test basically a function to run before and after the test
# # fixtures are user to feed data to the test such as database, api, etc
# # fixtures are used to run the test in a specific order



# function --> Run once per test
# class --> Run once per class of tests
# module --> Run once per module
# session --> Run once per session


class TestCustomUser:

    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="rik@gmail.com",
            password="12345678",
            first_name="John",
            last_name="Doe"
        )

    @pytest.fixture
    def receive_user(self):
        return CustomUser.objects.create_user(
            
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@gmail.com",
            "password": "1245678"
        )
         

    # @pytest.fixture
    # def test_user_create(self, user):
    #     assert user.email == "rik@gmail.com"
    #     assert user.first_name == "John"
    #     assert user.last_name == "Doe"
    #     assert user.is_active == True
    #     assert user.is_staff == False
    #     assert user.is_superuser == False

    @pytest.fixture
    def test_user_created(self):
        serilizer = CustomUserSerializer(data = self.user)
        assert serilizer.is_valid() == True
        serilizer.save()
        assert CustomUser.objects.count() == 1
        print("test_user_created")


    @pytest.fixture
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

        # assert bank.user.email == "

        


# @pytest.fixture(scope='session') # this is a decorator which makes the function a fixture
# def fixture1():
#     print(True)
#     return 1

# def test_example5(fixture1): # this is how you use a fixture
#     print(True)
#     num = fixture1 
#     assert num == 1


# def test_example6(fixture1): # this is how you use a fixture
#     print(True,'2')
#     num = fixture1 
#     assert num == 1
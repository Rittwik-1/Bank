# from accounts.views import login_view
# from django.test import TestCase,Client
# from django.urls import reverse,resolve
# from accounts.serializers import CustomUserSerializer
# from accounts.models import CustomUser
# from rest_framework.status import HTTP_201_CREATED

# # class TestUrls(TestCase):

# #     def setUp(cls):
# #         cls.client = Client()
# #         cls.customer_account_payload = {
# #             "first_name": "John",
# #             "last_name": "Doe",
# #             "email": "rikgmail.com",
# #             "password": "1245678",
# #             # 'password2': "1245678"
# #         }


# #         cls.login_payload = {
# #             "email": "rik@gmail.com",
# #             "password": "1245678"
# #         }


# #         cls.receiver_account_payload = {
# #             "first_name": "Jane",
# #             "last_name": "Doe",
# #             "email": "jane@gmail.com",
# #             "password": "1245678"
# #         }


# #     def test_login_user(self):
# #         response = self.client.post(reverse('login'), self.login_payload)
# #         self.assertEquals(response.status_code, 200)

# #     def test_register_user(self):
# #         response = self.client.post(reverse('register'), self.customer_account_payload)
# #         serializer = CustomUserSerializer(data=self.customer_account_payload)


# #         if response.status_code == HTTP_201_CREATED:
# #             user = CustomUser.objects.create_user(**self.customer_account_payload)
# #             self.assertTrue(serializer.is_valid())
# #             serializer.save()
# #             self.assertEquals(CustomUser.objects.count(), 1)



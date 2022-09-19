
from django.test import TestCase

from accounts.views import login_view

from django.urls import reverse,resolve
from banking.views import *
from http import HTTPStatus
from accounts.forms import Auth_from

from bankapp.urls import *

class TestUrls(TestCase):

    def test_login(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func,login_view)

    def test_register(self):
        url = reverse('register')
        # test a class based url
        self.assertEquals(resolve(url).func.view_class,CreateCustomUser)
         
        
    def test_dashboard(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func.view_class,CreateTransactionAPI)


    def test_createbankaccountapi(self):
        url = reverse('CreateBankAccountAPI')
        self.assertEquals(resolve(url).func.view_class,CreateBankAccountAPI)

    def test_transactions(self):
        url = reverse('transactions')
        self.assertEquals(resolve(url).func.view_class,transactions)

                
    def test_downloadbankaccounts(self):
        url = reverse('downloadbankaccounts')
        self.assertEquals(resolve(url).func,downloadBankAccounts)

    def test_createCard(self):
        url = reverse('createCard')
        self.assertEquals(resolve(url).func.view_class,createCard)

    def test_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class,views.LogoutView)

    def test_login_view(self):
        response = self.client.post(reverse('login'),{'email':'test@gmail.com','password':'test'})
        self.assertEquals(response.status_code,200)
         

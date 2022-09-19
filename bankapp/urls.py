
from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from banking.views import *

from iommi import Form
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views


app_name = 'bankapp'

urlpatterns = [
    path('admin/', admin.site.urls),

    # CREATE NEW USER VIA API
    path('register/', CreateCustomUser.as_view(),name="register"),

    # path('dashboard/', DashboardView.as_view(),name="index"),

    # API ENDPOINT TO SHOW ACCOUNT DETAILS FOR LOGGED-IN USER USING CUSTOMUSER SERIALIZER
    # path('viewuseraccount/', ViewUserAccount.as_view(),name="viewuseraccount"),
    

    path('createbankaccountapi/', CreateBankAccountAPI.as_view(),name = "CreateBankAccountAPI"),
    # path('createtransactionapi/', CreateTransactionAPI.as_view()),
    path('dashboard/', CreateTransactionAPI.as_view(),name="dashboard"),


    # API ENDPOINT TO SHOW ACCOUNT DETAILS FOR LOGGED-IN USER USING BANKACCOUNT SERIALIZER
    # path('viewbankaccountuser/', ViewBankAccountUser.as_view()),
    path('transactions/', transactions.as_view(),name="transactions"),
    
    # CSV DOWNLOAD
    path('downloadbankaccounts/', downloadBankAccounts,name="downloadbankaccounts"),
    path('createCard/', createCard.as_view(),name="createCard"),
    


    # path('', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', login_view, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),


    # path('iommi-form-test/', Form.create(auto__model=CustomUser).as_view()),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


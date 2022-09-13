"""bankapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('viewuseraccount/', ViewUserAccount.as_view(),name="viewuseraccount"),
    

    path('createbankaccountapi/', CreateBankAccountAPI.as_view()),
    # path('createtransactionapi/', CreateTransactionAPI.as_view()),
    path('dashboard/', CreateTransactionAPI.as_view(),name="dashboard"),


    # API ENDPOINT TO SHOW ACCOUNT DETAILS FOR LOGGED-IN USER USING BANKACCOUNT SERIALIZER
    path('viewbankaccountuser/', ViewBankAccountUser.as_view()),
    path('transactions/', transactions.as_view()),
    
    # CSV DOWNLOAD
    path('downloadbankaccounts/', downloadBankAccounts),


    # path('', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', login_view, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # DRF AUTH
    # path('api-auth/', include('rest_framework.urls')),
    # path('', include('rest_framework.urls')),

    # path('iommi-form-test/', Form.create(auto__model=CustomUser).as_view()),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


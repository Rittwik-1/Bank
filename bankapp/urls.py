
from django.contrib import admin
from django.urls import path, include
from accounts.views import CreateCustomUser,login_view
from banking.views import CreateBankAccountAPI,CreateTransactionAPI,transactions,downloadBankAccounts,createCard
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views


app_name = 'bankapp'

urlpatterns = [
    path('admin/', admin.site.urls),

    # CREATE NEW USER VIA API
    path('register/', CreateCustomUser.as_view(),name="register"),

    path('createbankaccountapi/', CreateBankAccountAPI.as_view(),name = "CreateBankAccountAPI"),

    path('dashboard/', CreateTransactionAPI.as_view(),name="dashboard"),

    path('transactions/', transactions.as_view(),name="transactions"),
    
    path('downloadbankaccounts/', downloadBankAccounts,name="downloadbankaccounts"),

    path('createCard/', createCard.as_view(),name="createCard"),
    
    path('', login_view, name='login'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


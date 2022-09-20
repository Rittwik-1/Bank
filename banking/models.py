from django.db import models
from django.urls import reverse
from django.conf import settings
from banking.constants import account_type, om_ch


"""
this model is to create a bank account
"""

class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bankaccount', on_delete=models.CASCADE, )
    account_type = models.CharField(max_length=20, choices=account_type, db_index=True )
    account_balance = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True, verbose_name='Transaction Date')

    def __str__(self):
        return self.account_type

    
"""
This model is used to do the transcation
"""

class Transactions(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE, )
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_transactions', on_delete=models.CASCADE, )
    transaction_amount = models.FloatField()
    ts_type = models.CharField(max_length=20,choices=om_ch,null=True,default=2)
    transaction_date = models.DateTimeField(auto_now_add=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receiver.first_name


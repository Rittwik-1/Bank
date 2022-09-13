from django import forms
from .models import Transactions
from django.core.exceptions import ValidationError
from django.forms import widgets

class TransactionsForm(forms.ModelForm):

    class Meta:
        model = Transactions
        fields = "__all__"

        widgets={
            'user':forms.Select(attrs={'class':'form-control','placeholder':"First Name"}),
            'account_type':forms.Select(attrs={'class':'form-control','placeholder':"First Name"}),
            'transaction_type':forms.Select(attrs={'class':'form-control','placeholder':"Last Name"}),
            'transaction_amount':forms.NumberInput(attrs={'class':'form-control','placeholder':"Amount"}),
        }

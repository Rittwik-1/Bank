from django import forms
from banking.models import Transactions


"""
This class is used to create a form for the Transactions model.
this contians the fields that are required for the Transactions model like the account_number and the amount
"""
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

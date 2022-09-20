from rest_framework import serializers
from accounts.models import CustomUser
from banking.models import BankAccount, Transactions


"""
This is the serializer for the user
"""
class TransactionSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),many=False) #user field
    account_type = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(),many=False)
    
    class Meta:
        model = Transactions
        fields = [ 'id', 'transaction_date', 'account_type', 'user', 'ts_type', 'transaction_amount']
        
"""
This is the serializer for the user to create a new account
"""

class BankAccountSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),many=False)
    accounttransactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = BankAccount
        fields = [ 'date', 'account_type', 'user', 'account_balance', 'accounttransactions']
        extra_kwargs = {
            'account_balance': {'read_only': True},
        }
            
from rest_framework import serializers
from .models import CustomUser
from banking.serializers import *


class CustomUserSerializer(serializers.ModelSerializer):
    
    bankaccount = BankAccountSerializer(many=True)
    transactions = TransactionSerializer(many=True )

    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'bankaccount', 'transactions' ]

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    



         
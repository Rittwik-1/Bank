from rest_framework import serializers
from .models import CustomUser
from banking.serializers import *


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()


        bank_data = [{
            'user': user.pk,
            'date': '2022-09-23 06:00:00.579058',
            'account_balance': 1000,
            'account_type': 'savings',
        }]

        bank = BankAccountSerializer(data=bank_data, many=True)
        if bank.is_valid():
            bank.save()
            # print(bank)
        
        
        transaction_data = [{
            'user': user.pk,
            'receiver': user.pk,
            'ts_type': 2,
            'transaction_amount': 9999,
            'transaction_date': '2022-09-23 06:00:00.579058',
        },
        {
            'user': user.pk,
            'receiver': user.pk,
            'ts_type': 3,
            'transaction_amount': 999,
            'transaction_date': '2022-09-23 06:00:00.579058',
        },
        
        
        ]
        
        
        
        transaction = TransactionSerializer(data=transaction_data, many=True)
 
        if transaction.is_valid():
            transaction.save()
       



        
        return user
    



         
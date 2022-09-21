from rest_framework import serializers
from accounts.models import CustomUser
from banking.serializers import CustomUser,BankAccountSerializer,TransactionSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    bankaccount = BankAccountSerializer(many=True, read_only=True, )
    transactions = TransactionSerializer(many=True, read_only=True, )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'bankaccount', 'transactions'] #required fields for the CustomUser model
        extra_kwargs = {
            "password":{"write_only":True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data) #create a new user if the user does not exist and gives a valid data
        user.set_password(password)
        user.save()

        return user



         
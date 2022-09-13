from rest_framework import generics
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BankAccount
from .forms import TransactionsForm
from django.db.models import F
from django.http.response import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
import json
from django.shortcuts import render

import requests



# CREATE BANK ACCOUNT VIA API
class CreateBankAccountAPI(generics.CreateAPIView):

    serializer_class = BankAccountSerializer
    # permission_classes = [permissions.IsAdminUser]  UNCOMMENT IF REQUIRED FOR ADMIN USERS ONLY
    
    def post(self, request):
        serializer = BankAccountSerializer(data=request.data)
                
        if serializer.is_valid():
            account_type = serializer.validated_data['account_type']
            if account_type == 'savings':
                serializer.validated_data['account_balance'] = 0           # INITIAL BALANCE
            elif account_type == 'credit':
                serializer.validated_data['account_balance'] = 0       # INITIAL BALANCE
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# UPDATE BANK ACCOUNT VIA API

class BankAccountUpdate(APIView):
 
    def get(self, request, pk):
        account = self.get_object(pk)
        serializer = BankAccountSerializer(account)
        return Response(serializer.data)

    def get_object(self, pk, ):
        
        try:
            user_id = self.request.data.get('user')
            return BankAccount.objects.get(pk=pk, user_id = user_id)    # THE USER ID AND ACCOUNT ID MUST MATCH AN EXISTING ACCOUNT
        except BankAccount.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        account = self.get_object(pk)
        serializer = BankAccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# MAKE DEPOSITS AND WITHDRAWALS VIA API

class CreateTransactionAPI(generics.CreateAPIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    serializer_class = TransactionSerializer
    # permission_classes = [permissions.IsAdminUser]        UNCOMMENT IF REQUIRED FOR ADMIN USERS ONLY
    def get(self, request):
        serializer = TransactionSerializer()
        form = TransactionsForm()
        return Response({'serializer': serializer,'form':form,"amount":request.user.bankaccount.all()[0].account_balance})

    def post(self, request):
        try:
            account_type = request.POST.get('transaction_type')
            transaction_amount = request.POST.get('transaction_amount')
            bank_act = BankAccount.objects.get(user=request.user)
            print(bank_act)
            
            if account_type == "deposit":
                bank_act.account_balance = F('account_balance') + transaction_amount
                bank_act.save()
                Transactions.objects.create(
                    user=request.user,
                    receiver=request.user,
                    transaction_amount=transaction_amount,
                    ts_type=2
                )
            
            elif account_type == "withdrawal":
                if bank_act.account_balance > 50 and bank_act.account_balance > float(transaction_amount):
                    bank_act.account_balance = F('account_balance') - transaction_amount
                    bank_act.save()
                    Transactions.objects.create(
                    user=request.user,
                    receiver=request.user,
                    transaction_amount=transaction_amount,
                    ts_type=3
                )
                else:
                    return HttpResponse("Sorry bank balance low, can't withdrawal",status=404)


            serializer = TransactionSerializer()
            form = TransactionsForm()
            return Response({'serializer': serializer,'form':form,"amount":request.user.bankaccount.all()[0].account_balance})
        except Exception as e:
            return HttpResponse(f"ERROR Invalid Credentials {e}",status=404)



# API ENDPOINT TO SHOW ACCOUNT DETAILS FOR LOGGED-IN USER USING BANKACCOUNT SERIALIZER
class ViewBankAccountUser(generics.ListAPIView):
    '''
    VIEW ACCOUNT INFO FOR LOGGED IN USER
    '''
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        logged_in_user = self.request.user     # FOR LOGGED IN USERS      
        queryset = logged_in_user.bankaccount.all()
        return queryset


import csv

def downloadBankAccounts(request):
    '''
    DOWNLOAD ACCOUNT INFO of the logged in user in a txt file
    
    ''' 
    logged_in_user = request.user
    queryset = logged_in_user.bankaccount.all()

    serializer = BankAccountSerializer(queryset, many=True)
    
    # data = json.dumps({
    #     'user_information':serializer.data,
    #      "transactions": [{"receiver":i.receiver.first_name,"amount":i.transaction_amount,"date":i.transaction_date.__str__()} for i in Transactions.objects.filter(user=request.user)]
    # })
   
    
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=bankaccounts.csv'
    
    writer = csv.writer(response)
    writer.writerow(["Sender","Receiver","Amount","Transactions Type","Date"])
    for i in Transactions.objects.filter(user=request.user,ts_type=2):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Deposit",i.transaction_date.__str__()])
    for i in Transactions.objects.filter(user=request.user,ts_type=3):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Withdraw",i.transaction_date.__str__()])
    for i in Transactions.objects.filter(receiver=request.user,ts_type=1):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Send",i.transaction_date.__str__()])

    return response





    
class transactions(generics.CreateAPIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'index.html'
        serializer_class = TransactionSerializer
        
        def get(self,request):
            return redirect("dashboard")


        def post(self,request):
            try:
                recevier_bank_act = CustomUser.objects.get(uuid=request.POST.get('user')).bankaccount.all()[0]
             
                current_user_bank_act = request.user.bankaccount.all()[0]
                amount = request.POST.get('transaction_amount')
       

                if current_user_bank_act.account_balance > 50 and current_user_bank_act.account_balance > float(amount):
                    current_user_bank_act.account_balance = F('account_balance') - amount
                    recevier_bank_act.account_balance = F('account_balance') + amount
                    
                    recevier_bank_act.save()
                    current_user_bank_act.save()
                    
                    Transactions.objects.create(ts_type=1,user=request.user,receiver=CustomUser.objects.get(uuid=request.POST.get('user')),transaction_amount=amount)
                    print(recevier_bank_act)
                    print(current_user_bank_act)
                    return redirect("dashboard")
                else:
                    return HttpResponse("Amount balance is low",status=404)
            except Exception as e:
                return HttpResponse("No user found",status=404)
                
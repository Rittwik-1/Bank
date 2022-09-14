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

    def put(self, request, pk, format=None):
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
            
                    
            # serializer = TransactionSerializer(data=request.data)
            # print(serializer.is_valid())       
            # if serializer.is_valid():
            #     user_id = serializer.validated_data['user']
            #     account_type = serializer.validated_data['account_type']
            #     transaction_type = serializer.validated_data['transaction_type']
            #     transaction_amount = serializer.validated_data['transaction_amount']
                # bank_account = BankAccount.objects.get(id=account_type.pk, user_id=user_id)
                
                            
                # if bank_account:   # CONFIRM IF THIS ACCOUNT EXISTS BEFORE MAKING ANY CHANGES
                #     if transaction_type == 'deposit':
                #         bank_account.account_balance = F('account_balance') + transaction_amount
                #         bank_account.save()
                #         serializer.save()
                #         return Response(status=status.HTTP_201_CREATED)
                        
                #     elif transaction_type == 'withdrawal':
                #         if bank_account.account_type == 'savings':
                #             if bank_account.account_balance > 50 and bank_account.account_balance > transaction_amount:
                #                 new_savings_balance = bank_account.account_balance - transaction_amount 
                #                 if new_savings_balance >= 50:                                                # CHECK THAT NEW BALANCE WON'T BE LESS THAN 50
                #                     bank_account.account_balance = F('account_balance') - transaction_amount
                #                     bank_account.save()
                #                     serializer.save()
                #                     return Response(status=status.HTTP_201_CREATED)
                #                 else:
                #                     return Response(status=status.HTTP_400_BAD_REQUEST)                            
                #             else:
                #                 return Response(status=status.HTTP_400_BAD_REQUEST)
                        
                #         elif bank_account.account_type == 'credit':
                #             if bank_account.account_balance > 0 :
                #                 new_credit_balance = bank_account.account_balance - transaction_amount
                #                 if new_credit_balance >= 0:                                              # CHECK THAT NEW BALANCE WON'T BE LESS THAN -20000
                #                     bank_account.account_balance = F('account_balance') - transaction_amount
                #                     bank_account.save()
                #                     serializer.save()
                #                     return Response(status=status.HTTP_201_CREATED)
                #                 else:
                #                     return Response(status=status.HTTP_400_BAD_REQUEST) 
                #             else:
                #                 return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = TransactionSerializer()
            form = TransactionsForm()
            return Response({'serializer': serializer,'form':form,"amount":request.user.bankaccount.all()[0].account_balance})
        except Exception as e:
            return HttpResponse(f"ERROR Invalid Credentials {e}",status=404)



# API ENDPOINT TO SHOW ACCOUNT DETAILS FOR LOGGED-IN USER USING BANKACCOUNT SERIALIZER
# class ViewBankAccountUser(generics.ListAPIView):
#     '''
#     VIEW ACCOUNT INFO FOR LOGGED IN USER
#     '''
#     serializer_class = BankAccountSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         logged_in_user = self.request.user     # FOR LOGGED IN USERS      
#         queryset = logged_in_user.bankaccount.all()
#         return queryset


import csv

def downloadBankAccounts(request):
    '''
    DOWNLOAD ACCOUNT INFO of the logged in user in a txt file
    
    ''' 
    
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=bankaccounts.csv'
    
    writer = csv.writer(response)
    writer.writerow(["Sender","Receiver","Amount","Transactions Type","Date"])
    
    for i in Transactions.objects.filter(user=request.user,ts_type=1).order_by('-transaction_date'):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Send Money",i.transaction_date.__str__()])
    
    for i in Transactions.objects.filter(user=request.user,ts_type=2).order_by('-transaction_date'):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Deposit",i.transaction_date.__str__()])
        
    for i in Transactions.objects.filter(user=request.user,ts_type=3).order_by('-transaction_date'):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Withdraw",i.transaction_date.__str__()])

    for i in Transactions.objects.filter(user=request.user,ts_type=4).order_by('-transaction_date'):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Credit Card",i.transaction_date.__str__()])
        
    for i in Transactions.objects.filter(receiver=request.user,ts_type=1).order_by('-transaction_date'):
        writer.writerow([i.user,i.receiver,i.transaction_amount,"Receive Money",i.transaction_date.__str__()])


    return response
    
class transactions(generics.CreateAPIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'index.html'
        serializer_class = TransactionSerializer
        
        def get(self,request):
            return redirect("dashboard")


        def post(self,request):
            try:
                recevier_bank_act = BankAccount.objects.get(user=CustomUser.objects.get(uuid=request.POST.get('user')))
                current_user_bank_act = BankAccount.objects.get(user=request.user)
                amount = request.POST.get('transaction_amount')
       

                if current_user_bank_act.account_balance > 50 and current_user_bank_act.account_balance > float(amount):
                    current_user_bank_act.account_balance = F('account_balance') - amount
                    recevier_bank_act.account_balance = F('account_balance') + amount
                    
                    recevier_bank_act.save()
                    current_user_bank_act.save()
                    
                    Transactions.objects.create(ts_type=1,user=request.user,
                                                receiver=CustomUser.objects.get(uuid=request.POST.get('user')),
                                                transaction_amount=amount)

                    return redirect("dashboard")
                else:
                    return HttpResponse("Amount balance is low",status=404)
            except Exception as e:
                    return HttpResponse(f"No user found {e}",status=404)


        

import random

class createCard(generics.CreateAPIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'index.html'
        serializer_class = TransactionSerializer
        
        def get(self,request):
            try:
                
                user = request.user 

                
                # if the balance is low user cannot buy credit card
                if user.bankaccount.all()[0].account_balance < 1000:
                    return HttpResponse("Balance is low",status=404)
                     
                elif not user.credit_card:
                    bank_act = user.bankaccount.all()[0]
                    bank_act.account_balance = F('account_balance') - 1000
                    user.credit_card = random.randint(0000000000000000,9999999999999999)
                    user.save()
                    bank_act.save()
                    Transactions.objects.create(user=request.user,receiver=request.user,transaction_amount=1000,ts_type=4)
                
                
                
                else:
                    return HttpResponse("Your have already buy credit card",status=404)
                    
            except Exception as e:
                    return HttpResponse("No user found",status=404)
                
            return redirect("dashboard")


            
                
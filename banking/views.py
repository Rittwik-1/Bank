from rest_framework import generics
from banking.serializers import BankAccountSerializer,TransactionSerializer,Transactions,CustomUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from banking.models import BankAccount
from rest_framework import status
from banking.constants import transaction_type_csv
from banking.forms import TransactionsForm
from django.db.models import F
from django.http.response import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
import csv
import random


# CREATE BANK ACCOUNT VIA API
class CreateBankAccountAPI(generics.CreateAPIView):

    serializer_class = BankAccountSerializer
    # permission_classes = [permissions.IsAdminUser]  UNCOMMENT IF REQUIRED FOR ADMIN USERS ONLY
    
    def post(self, request):
        
        self.initial_balance = 0
        serializer = BankAccountSerializer(data=request.data)
                
        if serializer.is_valid():   
            account_type = serializer.validated_data['account_type']
            if account_type == 'savings':
                serializer.validated_data['account_balance'] = self.initial_balance           # INITIAL BALANCE
            elif account_type == 'credit':
                serializer.validated_data['account_balance'] = self.initial_balance       # INITIAL BALANCE
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
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
        self.minimun_balance = 0
        try:
            account_type = request.POST.get('transaction_type')
            transaction_amount = request.POST.get('transaction_amount')
            bank_act = BankAccount.objects.get(user=request.user)
            
            if account_type == "deposit":
                bank_act.account_balance = F('account_balance') + transaction_amount
                bank_act.save()

                """
                This is the code for the transaction history for each user and it records the transaction type, amount and the balance
                for every transacation
                """
                Transactions.objects.create(
                    user=request.user,
                    receiver=request.user,
                    transaction_amount=transaction_amount,
                    ts_type=2 # 2 for deposit
                )
                
            
            elif account_type == "withdrawal":
                if bank_act.account_balance > self.minimun_balance and bank_act.account_balance > float(transaction_amount):
                    bank_act.account_balance = F('account_balance') - transaction_amount
                    bank_act.save()
                    Transactions.objects.create(
                    user=request.user,
                    receiver=request.user,
                    transaction_amount=transaction_amount,
                    ts_type=3 # 3 for withdrawal
                )
                
                else:
                    return HttpResponse("Sorry bank balance low, can't withdrawal",status=404)
            
            serializer = TransactionSerializer()
            form = TransactionsForm()

            """
            Resposne for the dashboard
            """
            return Response({
                
            'serializer': serializer,
            'form':form,
            "amount":request.user.bankaccount.all()[0].account_balance,
            'status':200
            
            })
        except Exception as e:
            return HttpResponse(f"ERROR Invalid Credentials {e}",status=404)


def downloadBankAccounts(request):
    '''
    DOWNLOAD ACCOUNT INFO of the logged in user in a txt file
    '''  
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=bankaccounts.csv'
    
    writer = csv.writer(response)
    writer.writerow(["Sender","Receiver","Amount","Transactions Type","Date"])

    for transaction in Transactions.objects.filter(user=request.user).order_by("-date_created"):
        transaction_type_ex = transaction_type_csv.get(transaction.ts_type)
        writer.writerow([transaction.user,transaction.receiver,transaction.transaction_amount,transaction_type_ex,transaction.transaction_date.__str__()])
    
    return response
    
class transactions(generics.CreateAPIView):

        """
            This is a class for sending money to other users.
        """
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'index.html'
        serializer_class = TransactionSerializer
        
        def get(self,request):
            return redirect("dashboard") # redirect to dashboard(home page for the user)


        def post(self,request):
            self.minimun_balance = 0
            """
                This is the post method for sending money to other users.
            """
            try:
                recevier_bank_act = BankAccount.objects.get(user=CustomUser.objects.get(uuid=request.POST.get('user')))
                current_user_bank_act = BankAccount.objects.get(user=request.user)
                amount = request.POST.get('transaction_amount')
       

                if current_user_bank_act.account_balance > self.minimun_balance and current_user_bank_act.account_balance > float(amount):
                    current_user_bank_act.account_balance = F('account_balance') - amount
                    recevier_bank_act.account_balance = F('account_balance') + amount
                    
                    recevier_bank_act.save()
                    current_user_bank_act.save()
                    
                    Transactions.objects.create(ts_type=1,user=request.user, # 1 for sending money 
                                                receiver=CustomUser.objects.get(uuid=request.POST.get('user')),
                                                transaction_amount=amount)
                

                    return redirect("dashboard")
                else:
                    return HttpResponse("Amount balance is low",status=404)
            except Exception as e:
                    return HttpResponse(f"No user found {e}",status=404)


    
class createCard(generics.CreateAPIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'index.html'
        serializer_class = TransactionSerializer
        
        def get(self,request):
            self.minimum_balance = 1000
            try:
                
                user = request.user 

                
                # if the balance is low user cannot buy credit card
                if user.bankaccount.all()[0].account_balance < self.minimum_balance:
                    return HttpResponse("Balance is low",status=404)
                     
                elif not user.credit_card:
                    bank_act = user.bankaccount.all()[0]
                    bank_act.account_balance = F('account_balance') - self.minimum_balance
                    user.credit_card = random.randint(0000000000000000,9999999999999999)
                    user.save()
                    bank_act.save()

                    Transactions.objects.create(
                    user=request.user,
                    receiver=request.user,
                    transaction_amount=1000,
                    ts_type=4)
                
                
                
                else:
                    return HttpResponse("Your have already buy credit card",status=HTTP_404_NOT_FOUND)
                    
            except Exception as e:
                    return HttpResponse("No user found",status=HTTP_404_NOT_FOUND)
                
            return redirect("dashboard")


            
                
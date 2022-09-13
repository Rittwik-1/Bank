from urllib import request

from banking.models import BankAccount
from .models import CustomUser
from .serializers import CustomUserSerializer
from .forms import Auth_from, UserForm
from rest_framework import generics
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.shortcuts import  render, redirect
from django.contrib.auth import views
from django.views.generic import TemplateView
from rest_framework import  status
# CREATE NEW USER VIA API

class CreateCustomUser(generics.CreateAPIView):
    '''
    CURL COMMAND TO CREATE NEW USER
    curl --data "email=newuser@pp.com&first_name=newuserfirstname&last_name=newuserfirstname&password=1234" http://127.0.0.1:8000/register/

    URL: http://127.0.0.1:8000/register/
    '''
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request):
        serializer = CustomUserSerializer()
        form = UserForm()
        
        return Response({'serializer': serializer,'form':form,})

    def post(self, request):
        serializer = CustomUserSerializer()
        form = UserForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            form.save()
            user = CustomUser.objects.filter(email=form.cleaned_data['email'])
            
            if user.exists():
                BankAccount.objects.create(user=user[0],account_type=request.POST.get("account_type"))
                
                
            return redirect(reverse_lazy('login'))
        return Response({'serializer': serializer,'form':form},status=status.HTTP_201_CREATED)



# API ENDPOINT TO SHOW ACCOUNT DETAILS FOR LOGGED-IN USER USING CUSTOMUSER SERIALIZER

class ViewUserAccount(generics.ListAPIView):
    '''
    VIEW ACCOUNT INFO FOR LOGGED IN USER:
    URL: 'http://127.0.0.1:8000/viewuseraccount/'
    
    '''
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        logged_in_user = self.request.user.id  
        queryset = CustomUser.objects.filter(id = logged_in_user)
        return queryset


class DashboardView(TemplateView):
    
    template_name = "index.html"


from django.contrib.auth import authenticate , login 
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            forms = Auth_from(request.POST)
            if forms.is_valid():
                user_model = authenticate(email=forms.cleaned_data['email'],password=forms.cleaned_data['password'])
                if user_model:
                    print(user_model)
                    login(request,user_model)
                    return redirect('dashboard')
            
        return render(request,"login.html")
    
    else:
       return redirect('dashboard')
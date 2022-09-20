from banking.models import BankAccount
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.forms import Auth_from, UserForm
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.shortcuts import  render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate , login 


# CREATE NEW USER VIA API
class CreateCustomUser(generics.CreateAPIView):
    """
    This is the view for creating a new user
    """
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request):
        serializer = CustomUserSerializer()
        form = UserForm() # A form bound to the POST data
        
        return Response({'serializer': serializer,'form':form})

    def post(self, request):
        serializer = CustomUserSerializer()
        form = UserForm(request.POST or None) # A form bound to the POST data
        print(request.POST)
        if form.is_valid():
            form.save()
            user = CustomUser.objects.filter(email=form.cleaned_data['email']) # Get the user object
            
            if user.exists():
                BankAccount.objects.create(user=user[0],account_type=request.POST.get("account_type"))# Create a bank account for the user
                
            return redirect(reverse_lazy('login'))
        return Response({'serializer': serializer,'form':form})


"""
This is the view for the dashboard
"""
class DashboardView(TemplateView):
    template_name = "index.html" # The template to be rendered


"""
This is the view for the login
"""
def login_view(request):
    if not request.user.is_authenticated: # Check if the user is not authenticated
        if request.method == "POST":
            forms = Auth_from(request.POST) # A form bound to the POST data
            if forms.is_valid():
                user_model = authenticate(email=forms.cleaned_data['email'],password=forms.cleaned_data['password'])
                if user_model:
                    login(request,user_model)
                    return redirect('dashboard') # Redirect to a success page.
            
        return render(request,"login.html")
    
    else:
       return redirect('dashboard')
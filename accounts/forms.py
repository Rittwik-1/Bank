from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.forms import widgets

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"Password"}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"Password Confirmation"}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','password1','password2')

        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':"First Name"}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':"Last Name"}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':"Email"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return 


class Auth_from(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

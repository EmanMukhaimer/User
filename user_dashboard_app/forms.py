from django import forms
from django.core import validators
from .models import User

def validate_mail(value):
    users=User.objects.all()
    if users.filter(email=value).exists():
        raise forms.ValidationError("This email already exist.")

class RegisterForm(forms.Form):
    email = forms.EmailField(validators =[validate_mail])
    first_name = forms.CharField(label='First Name:', min_length=2)
    last_name = forms.CharField(label='Last Name:', min_length=2)
    password = forms.CharField(min_length=8,label='Password',widget=forms.PasswordInput,required=True)
    conf_pass = forms.CharField(min_length=8,label='Password Confirmation',widget=forms.PasswordInput,required=True)
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8,label='Password',widget=forms.PasswordInput,required=True)
    
from django import forms
from django.forms import ModelForm
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from index.models import *
from .models import *


class RegisterForm(forms.Form):
    fullname = forms.CharField(label='Fullname')
    emailaddress = forms.CharField(label='Email')
    
    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        return fullname        
    
    def clean_emailaddress(self):
        emailaddress = self.cleaned_data['emailaddress']		
        if not re.search((r'[\w\+@/. ]+'), emailaddress):
            raise forms.ValidationError('Email is not in the correct format, check your @ symbol and your . symbol')
        reg = Register.objects.filter(emailaddress=emailaddress).last()
        if reg:
            raise forms.ValidationError('This Email Address has already been used to register.')
        else:
            return emailaddress
        return emailaddress
    

class RegisterConfirmForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput() )
    confirmpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput() )

    def clean_username(self):
        username = self.cleaned_data['username']		
        if not re.search(r'^\w+', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        
        user = User.objects.filter(username=username).last()
        if user:
            raise forms.ValidationError('Username is already taken.')
        else:
            return username

    def clean_confirmpassword(self):
        if 'password' in self.cleaned_data:		
            password = self.cleaned_data['password']
            confirmpassword = self.cleaned_data['confirmpassword']
            if password == confirmpassword:
                return confirmpassword
            raise forms.ValidationError('Passwords do not match.')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput() )
    
    def clean_username(self):
        username = self.cleaned_data['username']		
        try:
            User.objects.filter(username=username).last()
        except ObjectDoesNotExist:
            raise forms.ValidationError('Account does not exist.')
        return username

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')	
    def clean_email(self):
        email = self.cleaned_data['email']		
        if not re.search((r'[\w\+@/. ]+'), email):
            raise forms.ValidationError('Email is not in the correct format, check your @ symbol and your . symbol')
        try:
            User.objects.filter(email=email).last()
        except ObjectDoesNotExist:
            raise forms.ValidationError('Email is not registered with us yet.')
        return email

class ResetPasswordConfirmForm(forms.Form):
    newpassword = forms.CharField(label='Password', widget=forms.PasswordInput() )
    confirmpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput() )

    def clean_confirmpassword(self):
        if 'newpassword' in self.cleaned_data:		
            password = self.cleaned_data['newpassword']
            confirmpassword = self.cleaned_data['confirmpassword']
            if password == confirmpassword:
                return confirmpassword
            raise forms.ValidationError('Passwords do not match.')

class ProfileForm(ModelForm):
	class Meta:
		model = Accounts
		fields = ['photograph', 'fullname', 'phonenumber', 'gender']


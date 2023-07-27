from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder' : 'Input your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'placeholder': 'Input your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder' : 'Input your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder': 'Input your password confirmation'}))
    class Meta:
        model = User
        fields = ['username', 'email']

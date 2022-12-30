from django import forms
from api.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
            
        ]
        widgets={
            'first_name':forms.TextInput(attrs={"class":"form-control"}),
            'last_name':forms.TextInput(attrs={"class":"form-control"}),
            'username':forms.TextInput(attrs={"class":"form-control"}),
            'email':forms.EmailInput(attrs={"class":"form-control"}),
            'password1':forms.PasswordInput(attrs={"class":"form-control"}),
            'password2':forms.TextInput(attrs={"class":"form-control"})
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'image',
        ]

        widgets = {
            'title':forms.Textarea(attrs={"class":"form-control"}),
            'image':forms.FileInput(attrs={"class":"form-control"}),
        }
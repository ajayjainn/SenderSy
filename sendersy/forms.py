from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField()

    class Meta():
        model = User
        fields = ('username','password1', 'password2','first_name')


    

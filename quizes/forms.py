from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Creating a user form for register.html page
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 


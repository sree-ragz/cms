from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import *
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class Registration2Form(ModelForm):
    class Meta:
        model=Participant
        fields=['name','email','designation','organization','photo','ph_no','is_author']



class EditForm(ModelForm):
    class Meta:
        model=Participant
        fields=['name','email','designation','organization','photo','ph_no']
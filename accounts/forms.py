from django import forms
from django import forms
import django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import *


class CreateOrder(forms.ModelForm):#eger sifirdan bir form yaratmag isteyirsense forms.Form dan istifade etmelilsen
    class Meta:#Burdaki form vasitesile bir sifaris yaradirig
        model = Order
        fields = '__all__'#?Burdaki __all__ vasiteisle Order modelinde butun datalar bu forma gelecek

class RegisterForm(UserCreationForm):
    class Meta:
        model = User#=cunki UserCreation formdur
        fields = ['username','email','password1','password2']
        

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']#yeni user cixsin ordan usere el deymirik exclude edirik yeni devre disi buraxirig,yeni istisna edirik,fields,ve ya exclude lari liste icinde istifade et hemise xeta vermirler cunki
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        # fields = ('username', 'first_name', 'last_name', 'email')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['customer', 'complete']


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'

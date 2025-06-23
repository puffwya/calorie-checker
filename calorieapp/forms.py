from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FoodSearchForm(forms.Form):
    food_name = forms.CharField(label='Food name', max_length=100)
    # food_name = forms.cleaned_data['query']

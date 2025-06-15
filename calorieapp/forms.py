from django import forms

class FoodSearchForm(forms.Form):
    food_name = forms.CharField(label='Food name', max_length=100)
    # food_name = forms.cleaned_data['query']

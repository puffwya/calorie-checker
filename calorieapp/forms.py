from django import forms

class FoodSearchForm(forms.Form):
    query = forms.CharField(label='Food name', max_length=100)
    food_name = form.cleaned_data['query']

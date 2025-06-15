import requests
from django.shortcuts import render
from .forms import FoodSearchForm
from django.conf import settings

def food_search(request):
    calories = None
    error = None

    if request.method == 'POST':
        form = FoodSearchForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            api_key = 'QUBc42H7FmcWn3UA1LQ4mBZ7UOAWJ4UBk0bZopPx'
            search_url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}'
            
            try:
                response = requests.get(search_url)
                data = response.json()
                if data.get('foods'):
                    food_data = data['foods'][0]
                    calories = next(
                        (nutrient['value'] for nutrient in food_data['foodNutrients']
                         if nutrient['nutrientName'] == 'Energy'), None
                    )
                else:
                    error = "No food found."
            except Exception as e:
                error = f"Error contacting USDA API: {str(e)}"
    else:
        form = FoodSearchForm()

    return render(request, 'calorieapp/food_search.html', {
        'form': form,
        'calories': calories,
        'error': error
    })


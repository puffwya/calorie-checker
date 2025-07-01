import requests
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.conf import settings
from .forms import FoodSearchForm
from django.conf import settings
from .models import UserLog
from django.contrib.auth.decorators import login_required

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def food_search(request):
    calories = None
    error = None

    if request.method == 'POST':
        form = FoodSearchForm(request.POST)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            api_key = settings.USDA_API_KEY
            search_url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}'
            try:
                UserLog.objects.create(user=request.user,search_term=food_name,ip_address=get_client_ip(request))
            except Exception as e:
                print("Error saving log:", e)
            
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

@login_required
def user_log_history(request):
    logs = UserLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'calorieapp/user_log_history.html', {'logs': logs})

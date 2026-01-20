from django.shortcuts import render, redirect
from .models import Ingredient
from .forms import IngredientForm
# Create your views here.

def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, "meal_planning/list.html", {"ingredients": ingredients})

def add_ingredient(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ingredient-list")
    else:
        form = IngredientForm()

    return render(request, "meal_planning/add.html", {"form": form})
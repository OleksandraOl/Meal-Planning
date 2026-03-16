from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ingredient
from .forms import IngredientForm
from .ai_prompts import build_recipe_prompt
from .ai_functions import get_recipe_content_with_retries, AIServiceError

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

def get_recipe_suggestions(request):
    ingredients = Ingredient.objects.all()
    ingredients_for_api_call = ", ".join([f"{i.amount} {i.unit} of {i.name}" for i in ingredients])

    prompt = build_recipe_prompt(ingredients_for_api_call)

    try:
        recipes_returned = get_recipe_content_with_retries(prompt)

        if not recipes_returned:
            messages.info(request, "We couldn't find any recipes for those ingredients.")

    except AIServiceError as e:
        messages.error(request, str(e))
        recipes_returned = []

    return render(request, "meal_planning/recipes.html",
                  {'recipes': recipes_returned})

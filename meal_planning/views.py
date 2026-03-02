from django.shortcuts import render, redirect
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from dotenv import load_dotenv
import json
import os
from django.http import JsonResponse
from .models import Ingredient
from .forms import IngredientForm
# Create your views here.

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name = "gemini-3-flash-preview",
    system_instruction = "You are a recipe generator. Respond ONLY in valid JSON. No conversational filler.",
    generation_config=GenerationConfig(response_mime_type="application/json")
)

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

    prompt = f"""
        Based on these ingredients: {ingredients_for_api_call}, provide a recipe suggestions. 
        Return a list of objects where each object has keys: 
        "recipe_name", 
        "prep_time", 
        "list_of_ingredients" (a list of strings), 
        "instructions" (a list of steps).
    """

    response = model.generate_content(prompt)
    recipes_returned = json.loads(response.text)

    return render(request, "meal_planning/recipes.html",
                  {'recipes': recipes_returned})

from django.urls import path
from .views import ingredient_list, add_ingredient, get_recipe_suggestions

urlpatterns = [
    path("", ingredient_list, name="ingredient-list"),
    path("add/", add_ingredient, name="add-ingredient"),
    path("generate-recipe/", get_recipe_suggestions, name="generate-recipe")
]
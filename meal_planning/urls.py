from django.urls import path
from .views import ingredient_list, add_ingredient

urlpatterns = [
    path("", ingredient_list, name="ingredient-list"),
    path("add/", add_ingredient, name="add-ingredient"),
]
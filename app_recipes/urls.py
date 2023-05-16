from django.urls import path
from .views import ai_recipe

urlpatterns = [
    # path('recipe/', generate_recipe_and_image, name='recipe-and-image'),
    path('', ai_recipe, name='ai-recipe'),
]

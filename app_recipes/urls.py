from django.urls import path
from .views import ai_recipe


urlpatterns = [
    path('recipe/', ai_recipe, name='recipe-and-image'),
    path('', ai_recipe, name='ai-recipe'),
]

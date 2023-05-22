from django.urls import path, include
from .views import ai_recipe
from . import views


urlpatterns = [
    path('recipe/', ai_recipe, name='recipe-and-image'),
    path('', ai_recipe, name='ai-recipe'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]

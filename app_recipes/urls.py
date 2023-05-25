from django.urls import path, include
from .views import ai_recipe
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:recipe_id>', views.recipe, name='recipe'),
    path('search/', views.search, name='search'),
    path('generate/', ai_recipe, name='generate'),
    path('like_recipe/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
    path('myrecipes/', views.RecipesByUserListView.as_view(), name='my-recipes'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]

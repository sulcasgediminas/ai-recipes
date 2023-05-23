from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.forms import User
from django.http import HttpResponse

import openai
import os

import base64
import requests
from django.http import JsonResponse
import html
from django.core.files.base import ContentFile
import urllib.request

from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.views import generic


openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the function to generate a recipe and an image
def ai_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            cuisine = form.cleaned_data['cuisine']

            # Generate the recipe and image using OpenAI API
            recipe_prompt = f"<br>Begin with generating list of ingredients, including measurements(using those ingredients {ingredients} plus add extra needed and use {cuisine} cuisine). <br>After, describe the preparation steps, including cooking time and temperatures. <br>Finally, provide any suggestions for serving or plating the dish."
            recipe_completion = openai.Completion.create(
                model="text-davinci-003",
                prompt=recipe_prompt,
                max_tokens=512,
                temperature=0.5,
                n= 1,
            )
            recipe_text = recipe_completion.choices[0].text.strip()

            # Generate the title using OpenAI API
            title_prompt = f"<br>Generate a title for the recipe using the generated recipe:<br>{recipe_text}"
            title_completion = openai.Completion.create(
                model="text-davinci-003",
                prompt=title_prompt,
                max_tokens=512,
                temperature=0.5
            )
            title_text = title_completion.choices[0].text.strip()

            # recipe = Recipe.objects.create(name=title_text, user=request.user)

            # Generate the image using OpenAI API
            image_prompt = f"dish of {ingredients} from {cuisine}."
            image_completion = openai.Image.create(
                prompt=image_prompt,
                size="256x256",
                n=1,
            )
            image_url = image_completion["data"][0]["url"]

            image_response = requests.get(image_url)
            image_content = image_response.content
            image_base64 = base64.b64encode(image_content).decode("utf-8")

            # Pass the generated recipe and image to the template
            context = {
                "title": title_text,
                "recipe": recipe_text,
                "image_base64": image_base64,
            }

            recipe = form.save(commit=False)
            user = request.user
            title = title_text

            recipe = Recipe(user=user, name=title, cuisine=cuisine, ingredients=ingredients, instructions=recipe_text)
            recipe.image_file.save(f"{title_text}.jpg", ContentFile(urllib.request.urlopen(image_url).read()))
            recipe.save()

            return render(request, "recipe_and_image.html", context)

    else:
        form = RecipeForm()
    return render(request, 'generate_form.html', {'form': form})



@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')




def index(request):
    num_recipes = Recipe.objects.all().count()

    context = {
        'num_recipes': num_recipes,
    }

    return render(request, 'index.html', context=context)

def recipes(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes.html', context=context)

def recipe(request, recipe_id):
    single_recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe.html', {'recipe': single_recipe})

def search(request):
    query = request.GET.get('query')
    search_results = Recipe.objects.filter(Q(name__icontains=query) | Q(ingredients__icontains=query))
    return render(request, 'search.html', {'recipes': search_results, 'query': query})

from django.contrib.auth.mixins import LoginRequiredMixin

class RecipesByUserListView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'user_recipes.html'
    paginate_by = 3

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user).order_by('uploaded_at')


from django.shortcuts import render
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.forms import User


import openai
import os

import base64
import requests
from django.http import JsonResponse


openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the function to generate a recipe and an image
def ai_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            cuisine = form.cleaned_data['cuisine']

            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            # Generate the recipe and image using OpenAI API
            recipe_prompt = f"\nBegin with creating a title of recipe. \nThen, generate list of ingredients, including measurements(using those ingredients {ingredients} plus add extra needed and use {cuisine} cuisine). \nAfter, describe the preparation steps, including cooking time and temperatures. \nFinally, provide any suggestions for serving or plating the dish."
            # recipe_prompt = f"Start with a title for the recipe. Generate a recipe using the following ingredients: {ingredients}. The cuisine should be {cuisine}. Please provide clear and concise instructions for the recipe. \nBegin with a list of ingredients, including measurements. \nThen, describe the preparation steps, including cooking times and temperatures. \nFinally, provide any suggestions for serving or plating the dish. Use simple and concise language that is easy to follow. Avoid unnecessary or overly complicated language."
            recipe_completion = openai.Completion.create(
                engine="davinci",
                prompt=recipe_prompt,
                max_tokens=512,
                n=1,
                stop=None,
                temperature=0.7,
            )
            recipe_text = recipe_completion.choices[0].text.strip()
            # Replace \n characters with <br> tags for line breaks
            recipe_text = recipe_text.replace('\n', '<br>')

            # image_prompt = f"dish of {ingredients} from {cuisine}"
            # image_completion = openai.Image.create(
            #     prompt=image_prompt,
            #     size="256x256",
            #     n=1,
            # )
            # image_url = image_completion["data"][0]["url"]

            # image_response = requests.get(image_url)
            # image_content = image_response.content
            # image_base64 = base64.b64encode(image_content).decode("utf-8")

            # Pass the generated recipe and image to the template
            context = {
                "recipe": recipe_text,
                # "image_base64": image_base64,
            }
            return render(request, "recipe_and_image.html", context)

    else:
        form = RecipeForm()
    return render(request, 'recipe_form.html', {'form': form})
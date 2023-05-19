from django.shortcuts import render
from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.forms import User


import openai
import os

import base64
import requests
from django.http import JsonResponse
import html
from django.core.files.base import ContentFile
import urllib.request


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
            # recipe_prompt = f"Start with a title for the recipe. Generate a recipe using the following ingredients: {ingredients}. The cuisine should be {cuisine}. Please provide clear and concise instructions for the recipe. \nBegin with a list of ingredients, including measurements. \nThen, describe the preparation steps, including cooking times and temperatures. \nFinally, provide any suggestions for serving or plating the dish. Use simple and concise language that is easy to follow. Avoid unnecessary or overly complicated language."
            recipe_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": recipe_prompt}
                ]
            )
            recipe_text = recipe_completion.choices[0].message['content']
            formatted_content = html.escape(recipe_text)
            formatted_content = formatted_content.replace('\n', '<br>')
            formatted_content = f'<pre>{formatted_content}</pre>'

            # Generate the title using OpenAI API
            title_prompt = f"<br>Generate a title for the recipe using the generated recipe:<br>{formatted_content}"
            title_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": title_prompt}
                ]
            )
            title_text = title_completion.choices[0].message['content']
            formatted_title = html.escape(title_text)
            formatted_title = formatted_title.replace('\n', '<br>')
            formatted_title = f'<pre>{formatted_title}</pre>'
            # recipe = Recipe.objects.create(title=title_text, user=request.user)

            # Generate the image using OpenAI API
            image_prompt = f"dish of {ingredients} from {cuisine}"
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
                "recipe": formatted_content,
                "image_base64": image_base64,
            }

            recipe = form.save(commit=False)
            user = request.user
            title = title_text

            recipe = Recipe(user=user, name=title, cuisine=cuisine, ingredients=ingredients)
            recipe.image_file.save(f"{title_text}.jpg", ContentFile(urllib.request.urlopen(image_url).read()))
            recipe.save()

            return render(request, "recipe_and_image.html", context)

    else:
        form = RecipeForm()
    return render(request, 'recipe_form.html', {'form': form})
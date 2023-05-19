from django.contrib import admin
from .models import Recipe
from django.utils.html import format_html
# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingredients', 'user', 'cuisine', 'image_thumbnail')
    def image_thumbnail(self, obj):
        return format_html(f'<img src="{obj.image_file.url}" width="100" height="100" />')
    image_thumbnail.short_description = 'Thumbnail'

admin.site.register(Recipe, RecipeAdmin)
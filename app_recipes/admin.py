from django.contrib import admin
from .models import Recipe
from django.utils.html import format_html
# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ingredients', 'user', 'cuisine', 'image_thumbnail', 'display_likes')
    list_filter = ('ingredients', 'user', 'cuisine')
    search_fields = ('ingredients', 'name')

    def image_thumbnail(self, obj):
        if obj.image_file:
            return format_html(f'<img src="{obj.image_file.url}" width="100" height="100" />')
        else:
            default_image_url = '/media/images/default.jpeg'  # Replace with the URL of your default image
            return format_html(f'<img src="{default_image_url}" width="100" height="100" />')

    image_thumbnail.short_description = 'Thumbnail'

    def display_likes(self, obj):
        return obj.likes.count()



admin.site.register(Recipe, RecipeAdmin)


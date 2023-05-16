from django.db import models
from django.conf import settings

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=200, blank=True, null=True)
    ingredients = models.CharField(max_length=200)
    instructions = models.TextField()
    image_file = models.ImageField(upload_to='media/images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            self.user = user
        super().save(*args, **kwargs)

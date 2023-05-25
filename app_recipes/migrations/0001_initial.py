# Generated by Django 4.2.1 on 2023-05-25 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cuisine', models.CharField(blank=True, max_length=200, null=True)),
                ('ingredients', models.CharField(max_length=200)),
                ('instructions', models.TextField()),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_recipes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

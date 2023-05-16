# Generated by Django 4.2.1 on 2023-05-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_recipes', '0002_alter_recipe_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cuisine',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]

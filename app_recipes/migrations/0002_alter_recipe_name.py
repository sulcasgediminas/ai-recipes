# Generated by Django 4.2.1 on 2023-05-12 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=2000),
        ),
    ]
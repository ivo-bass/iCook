# Generated by Django 3.2.5 on 2021-07-29 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_views',
            field=models.IntegerField(default=0),
        ),
    ]
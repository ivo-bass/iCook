# Generated by Django 3.2.5 on 2021-08-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dark_theme',
            field=models.BooleanField(default=False),
        ),
    ]

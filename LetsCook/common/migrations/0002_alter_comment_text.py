# Generated by Django 3.2.5 on 2021-07-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=300),
        ),
    ]

# Generated by Django 3.2.5 on 2021-08-05 12:50

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210805_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], default='food-default.png', force_format='JPEG', keep_meta=True, null=True, quality=75, size=[680, 382], upload_to='recipes'),
        ),
    ]
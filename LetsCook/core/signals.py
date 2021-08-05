import os

from cloudinary import uploader
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from LetsCook.profiles.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    # if the user is initialized attach a new profile to it
    if created:
        # activate superuser
        if instance.is_superuser:
            instance.is_active = True
            instance.save()

        profile = Profile(
            user=instance,
        )
        # set default username to be the domain name
        default_username = instance.email.split('@')[0]
        # if the username exists add pk
        if Profile.objects.filter(username=default_username).exists():
            default_username += str(instance.pk)
        profile.username = default_username
        profile.save()


@receiver(pre_delete, sender=UserModel)
def user_deleted(sender, instance, **kwargs):
    image = instance.profile.image
    if image:
        image_path = image.public_id
        uploader.destroy(image_path)


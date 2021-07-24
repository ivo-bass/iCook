from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from LetsCook.profiles.models import Profile
from LetsCook.recipes.models import Recipe

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    # if the user is initialized attach a new profile to it
    if created:
        profile = Profile(
            user=instance,
        )
        # set default username to be the domain + user's id
        default_username = instance.email.split('@')[0] + str(instance.pk)
        profile.username = default_username
        profile.save()

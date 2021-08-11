from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class SignalCreateUserTest(TestCase):
    def test_superuserCreated_isActive(self):
        superuser = UserModel.objects.create_superuser(email='test@test.test', password='qwe987qwe987')
        self.assertTrue(superuser.is_active)


"""
@receiver(pre_delete, sender=UserModel)
def user_deleted(sender, instance, **kwargs):
    image = instance.profile.image
    if image:
        image_path = image.public_id
        uploader.destroy(image_path)
"""


class SignalDeleteUserTest(TestCase):
    # tested in delete user view
    pass


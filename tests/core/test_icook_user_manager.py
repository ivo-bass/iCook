from django.contrib.auth import get_user_model
from django.test import TestCase


UserModel = get_user_model()


class ICookUserManagerTest(TestCase):
    # regular user is tested in model tests
    def test_userManager_whenSuperUserIsCreated(self):
        superuser = UserModel.objects.create_superuser(email='test@test.test', password='qwe987qwe987')
        user = UserModel.objects.first()
        self.assertEqual(user.id, superuser.id)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

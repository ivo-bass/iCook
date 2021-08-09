from django.test import TestCase

from tests.base.testing_utils.create_user_objects import create_regular_user


class UserModelTest(TestCase):
    def test_regularUserInit(self):
        user = create_regular_user()
        self.assertEqual('test@test.test', user.email)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        date_exists = user.date_joined is not None
        self.assertTrue(date_exists)
        self.assertIsNotNone(user.profile)

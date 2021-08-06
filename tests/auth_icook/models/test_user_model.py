from django.test import TestCase

from tests.base.create_user_objects import create_regular_user


class UserModelTest(TestCase):
    def setUp(self):
        self.user = create_regular_user()

    def test_regularUserInit(self):
        self.assertEqual('test@test.test', self.user.email)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        date_exists = self.user.date_joined is not None
        self.assertTrue(date_exists)

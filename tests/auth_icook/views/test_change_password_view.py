from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.base.main_test_case import MainTestCase

UserModel = get_user_model()


class ChangePasswordViewTest(MainTestCase):
    def test_changePassword_whenUserIsNotLoggedIn_shouldRedirectToSignIn(self):
        response = self.client.get(reverse('change-password'))
        self.assertEqual(302, response.status_code)
        self.assertEqual('/auth/sign-in/?next=/auth/change-password/', response.headers['location'])

    def test_changePasswordValid_shouldChangePasswordAndRedirectToUpdateProfile(self):
        self.client.login(username=self.EMAIL, password=self.PASSWORD)
        user = auth.get_user(self.client)
        old_pass = user.password
        response = self.client.post(
            reverse('change-password'),
            data={
                'old_password': self.PASSWORD,
                'new_password1': 'asd321asd321',
                'new_password2': 'asd321asd321',
            }
        )
        user = auth.get_user(self.client)
        new_pass = user.password
        self.assertNotEqual(old_pass, new_pass)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('update-profile'), response.headers['location'])


    def test_changePasswordInvalid_shouldHaveErrors(self):
        self.client.login(username=self.EMAIL, password=self.PASSWORD)
        user = auth.get_user(self.client)
        old_pass = user.password
        response = self.client.post(
            reverse('change-password'),
            data={
                'old_password': self.PASSWORD,
                'new_password1': 'asd321asd321',
                'new_password2': '321asd321asd',
            }
        )
        user = auth.get_user(self.client)
        new_pass = user.password
        self.assertEqual(old_pass, new_pass)
        self.assertEqual(200, response.status_code)
        errors = response.context['form'].errors['new_password2']
        self.assertIn('The two password fields didn’t match.', errors)

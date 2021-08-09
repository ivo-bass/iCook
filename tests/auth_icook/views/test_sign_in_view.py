from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class SignInViewTest(MainTestCase):
    def test_signInSuccess_shouldRedirectToHome(self):
        response = self.client.post(reverse('sign-in'), data={'username': 'test@test.test', 'password': 'qwe987qwe987'})
        self.assertEqual(302, response.status_code)
        self.assertEqual('/profile/home/', response.headers['location'])

    def test_wrong_username(self):
        response = self.client.post(reverse('sign-in'), {'username': 'wrong', 'password': 'qwe987qwe987'})
        self.assertEqual(200, response.status_code)
        errors = response.context_data['form'].errors['password']
        default_error = 'Please enter a correct email and password. Note that both fields may be case-sensitive.'
        self.assertIn(default_error, errors)

    def test_wrong_password(self):
        response = self.client.post(reverse('sign-in'), {'username': 'test@test.test', 'password': 'wrong'})
        self.assertEqual(200, response.status_code)
        errors = response.context_data['form'].errors['password']
        default_error = 'Please enter a correct email and password. Note that both fields may be case-sensitive.'
        self.assertIn(default_error, errors)

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class SignInViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.test', password='qwe987qwe987',)
        self.user.is_active = True
        self.user.save()

    def tearDown(self):
        self.user.delete()

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

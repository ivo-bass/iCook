from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class SignOutViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@test.test', password='qwe987qwe987',)
        self.user.is_active = True
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_signOut_whenUserIsNotLoggedIn_shouldRedirectToSignIn(self):
        response = self.client.post(reverse('sign-out'))
        self.assertEqual(302, response.status_code)
        self.assertEqual('/auth/sign-in/?next=/auth/sign-out/', response.headers['location'])

    def test_signOut_shouldRedirectToIndex(self):
        is_logged_in = self.client.login(username='test@test.test', password='qwe987qwe987')
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse('sign-out'), follow=False)
        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.headers['location'])

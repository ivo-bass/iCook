from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.base.main_test_case import MainTestCase

UserModel = get_user_model()


class SignOutViewTest(MainTestCase):
    def tearDown(self):
        self.user.delete()

    def test_signOut_whenUserIsNotLoggedIn_shouldRedirectToSignIn(self):
        response = self.client.post(reverse('sign-out'))
        self.assertEqual(302, response.status_code)
        self.assertEqual('/auth/sign-in/?next=/auth/sign-out/', response.headers['location'])

    def test_signOutSuccess_shouldRedirectToIndex(self):
        is_logged_in = self.client.login(username=self.EMAIL, password=self.PASSWORD)
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse('sign-out'), follow=False)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('index'), response.headers['location'])

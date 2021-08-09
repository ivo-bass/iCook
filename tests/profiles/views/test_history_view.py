from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class HistoryViewTest(MainTestCase):
    def test_history_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.post(reverse('history'))
        self.assertRedirects(response, '/auth/sign-in/?next=/profile/history/')


    def test_history_whenLoggedIn_shouldRenderTemplateAndChoices(self):
        self.create_recipe()
        self.create_choice()
        self.client.force_login(self.user)
        response = self.client.get(reverse('history'))
        choices = response.context.get('recipes_for_today')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profiles/history.html')
        self.assertNotEqual([], choices)
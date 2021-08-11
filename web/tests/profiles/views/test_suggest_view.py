import datetime

from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class SuggestViewTest(MainTestCase):
    def test_suggest_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.get(reverse('suggest'))
        self.assertRedirects(response, '/auth/sign-in/?next=/profile/suggest/')


    def test_suggestGet_whenLoggedIn_shouldRenderTemplateAndLikedRecipes(self):
        self.create_recipe()
        self.client.force_login(self.user)

        response = self.client.get(reverse('suggest'))
        suggestion_recipe_pk = response.context.get('recipe').pk

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profiles/suggest.html')
        self.assertEqual(self.recipe.pk, suggestion_recipe_pk)

    def test_suggestPost_shouldMakeChoice(self):
        self.create_recipe()
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('suggest'),
            data={
                'recipe-pk': self.recipe.pk,
                'date': datetime.date.today()
            }
        )
        user_choices_count = self.user.choice_set.count()

        self.assertEqual(302, response.status_code)
        self.assertNotEqual(0, user_choices_count)
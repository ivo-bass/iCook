from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class DeleteRecipeViewTest(MainTestCase):
    def test_deleteRecipe_whenAnonymous_shouldRedirectWithNext(self):
        self.create_recipe()
        response = self.client.post(reverse('delete-recipe', args=(self.recipe.pk,)))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, f'/auth/sign-in/?next=/recipe/delete/{self.recipe.pk}')

    def test_deleteRecipe_whenLoggedIn_shouldDelete(self):
        self.create_recipe()
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete-recipe', args=(self.recipe.pk,)))
        recipes_count = self.user.recipe_set.count()
        self.assertEqual(0, recipes_count)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('my-recipes'))

    def test_deleteRecipe_withCancel_shouldNotDelete(self):
        self.create_recipe()
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete-recipe', args=(self.recipe.pk,)),
            data={
                'cancel': 'cancel'
            }
        )
        recipes_count = self.user.recipe_set.count()
        self.assertEqual(1, recipes_count)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, f'/recipe/details/{self.recipe.pk}')


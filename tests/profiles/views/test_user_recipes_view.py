from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class UserRecipesViewTest(MainTestCase):
    def test_userRecipes_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.get(reverse('my-recipes'))
        self.assertRedirects(response, '/auth/sign-in/?next=/profile/my-recipes/')


    def test_userRecipes_whenLoggedIn_shouldRenderTemplateAndOwnRecipes(self):
        self.create_recipe()
        self.client.force_login(self.user)

        response = self.client.get(reverse('my-recipes'))
        recipe_pk = response.context.get('object_list')[0].pk

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profiles/my-recipes.html')
        self.assertEqual(self.recipe.pk, recipe_pk)
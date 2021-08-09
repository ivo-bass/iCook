from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class LikedRecipesViewTest(MainTestCase):
    def test_likedRecipes_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        self.create_like()
        response = self.client.get(reverse('liked-recipes'))
        self.assertRedirects(response, '/auth/sign-in/?next=/profile/liked-recipes/')


    def test_likedRecipes_whenLoggedIn_shouldRenderTemplateAndLikedRecipes(self):
        self.create_recipe()
        self.create_like()
        self.client.force_login(self.user)

        response = self.client.get(reverse('liked-recipes'))
        recipe_pk = response.context.get('object_list')[0].recipe.pk

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profiles/liked-recipes.html')
        self.assertEqual(self.recipe.pk, recipe_pk)
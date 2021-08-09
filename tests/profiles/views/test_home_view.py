from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class HomeViewTest(MainTestCase):
    def test_home_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.post(reverse('home'))
        self.assertRedirects(response, '/auth/sign-in/?next=/profile/home/')


    def test_home_whenLoggedIn_shouldRenderTemplateTopRecipesAndChoices(self):
        self.create_recipe()
        self.create_like()
        self.create_comment()
        self.create_choice()
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        recipe_most_views = response.context.get('most_views')
        recipe_most_likes = response.context.get('most_likes')
        recipe_most_comments = response.context.get('most_comments')
        choices = response.context.get('recipes_for_today')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profiles/home.html')
        self.assertEqual(self.recipe.id, recipe_most_views.id)
        self.assertEqual(self.recipe.id, recipe_most_likes.id)
        self.assertEqual(self.recipe.id, recipe_most_comments.id)
        self.assertNotEqual([], choices)
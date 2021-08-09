from django.urls import reverse

from LetsCook.core.constants import CATEGORIES
from tests.base.main_test_case import MainTestCase


class CreateRecipeViewTest(MainTestCase):
    def test_createRecipeGet_whenAnonymous_shouldRedirectToSignInWithNext(self):
        response = self.client.get(reverse('create-recipe'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/auth/sign-in/?next=/recipe/create/')

    def test_createRecipeGet_whenLoggedIn_shouldRenderTemplate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create-recipe'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'recipes/create.html')

    def test_createRecipePost_shouldCreateRecipe(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('create-recipe'),
            data={
                'title': 'test title',
                'meal_type': CATEGORIES[0],
                'description': 'test description',
                'preparation': 'test preparation',
                'time': 1,
                'servings': 1,
            }
        )
        user_recipes_count = self.user.recipe_set.count()
        self.assertNotEqual(0, user_recipes_count)
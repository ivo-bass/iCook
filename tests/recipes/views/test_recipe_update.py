from django.urls import reverse

from LetsCook.core.constants import CATEGORIES
from LetsCook.recipes.models import Recipe
from tests.base.main_test_case import MainTestCase


class UpdateRecipeViewTest(MainTestCase):
    def test_updateRecipeGet_whenAnonymous_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.get(reverse('update-recipe', args=(self.recipe.pk,)))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/auth/sign-in/?next=/recipe/update/1')

    def test_updateRecipeGet_whenLoggedIn_shouldRenderTemplate(self):
        self.client.force_login(self.user)
        self.create_recipe()
        response = self.client.get(reverse('update-recipe', args=(self.recipe.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'recipes/update.html')

    def test_updateRecipePost_shouldCreateRecipe(self):
        self.client.force_login(self.user)
        self.create_recipe()
        response = self.client.post(
            reverse('update-recipe', args=(self.recipe.pk,)),
            data={
                'author': self.user,
                'title': 'new title',
                'meal_type': CATEGORIES[-1],
                'description': 'new description',
                'preparation': 'new preparation',
                'time': 100,
                'servings': 100,
            }
        )
        recipe = Recipe.objects.first()
        all_recipes_count = len(Recipe.objects.all())
        self.assertEqual('new title', recipe.title)
        self.assertEqual(1, all_recipes_count)
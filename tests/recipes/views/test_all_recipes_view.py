from django.urls import reverse

from LetsCook.core.constants import CATEGORIES
from tests.base.main_test_case import MainTestCase


class AllRecipesViewTest(MainTestCase):
    def test_allRecipesGet_whenAnonymousUser_shouldRenderTemplate(self):
        self.create_recipe()
        response = self.client.get(reverse('all-recipes'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'recipes/all-recipes.html')

    def test_allRecipesGet_whenLoggedInUser_shouldRenderTemplate(self):
        self.create_recipe()
        response = self.client.get(reverse('all-recipes'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'recipes/all-recipes.html')

    def test_detailsRecipeGet_shouldShowOnlyPublicRecipes(self):
        self.create_recipe()
        self.create_private_recipe()
        response = self.client.get(reverse('all-recipes'))
        recipes = response.context.get('recipes')
        self.assertIsNotNone(recipes)
        self.assertEqual(1, len(recipes))

    def test_detailsRecipeGet_whenFilter_withEmptyCategory_shouldShowNothing(self):
        self.create_recipe()
        response = self.client.get(
            reverse('all-recipes'),
            data={
                'category': CATEGORIES[-1]
            }
        )
        recipes = response.context.get('recipes')
        self.assertEqual(0, len(recipes))

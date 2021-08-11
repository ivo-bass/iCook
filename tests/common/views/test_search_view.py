from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class SearchViewTest(MainTestCase):
    def test_search_whenNoKeyWord_shouldRenderTemplate(self):
        response = self.client.get(reverse('search'), data={'searched': ''})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'common/search.html')

    def test_search_whenKeyWordMatch_shouldPostRecipe(self):
        self.create_recipe()
        response = self.client.post(reverse('search'), data={'searched': self.recipe.title})
        self.assertEqual(200, response.status_code)
        recipe_search_title = response.context.get('searched')
        recipe_found = response.context.get('recipes').pop()
        self.assertEqual(recipe_search_title, recipe_found.title)

    def test_search_whenKeyWordDoesNotMatch_shouldNotPostRecipes(self):
        self.create_recipe()
        response = self.client.post(reverse('search'), data={'searched': 'nothing to match'})
        self.assertEqual(200, response.status_code)
        recipe_search_title = response.context.get('searched')
        recipes_found = response.context.get('recipes')
        self.assertEqual('nothing to match', recipe_search_title)
        self.assertSetEqual(set(), recipes_found)
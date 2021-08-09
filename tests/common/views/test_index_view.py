from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class IndexViewTest(MainTestCase):
    def test_index_shouldRenderTemplateAndTopRecipe(self):
        self.create_recipe()
        self.create_like()
        self.create_comment()
        response = self.client.get(reverse('index'))
        recipe_most_views = response.context.get('most_views')
        recipe_most_likes = response.context.get('most_likes')
        recipe_most_comments = response.context.get('most_comments')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'common/index.html')
        self.assertEqual(self.recipe.id, recipe_most_views.id)
        self.assertEqual(self.recipe.id, recipe_most_likes.id)
        self.assertEqual(self.recipe.id, recipe_most_comments.id)

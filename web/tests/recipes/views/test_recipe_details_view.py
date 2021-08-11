import datetime

from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class DetailsRecipeViewTest(MainTestCase):
    def test_detailsRecipeGet_whenAnonymousUser_shouldRenderTemplate(self):
        self.create_recipe()
        response = self.client.get(reverse('details-recipe', args=(self.recipe.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'recipes/details.html')

    def test_detailsRecipeGet_whenLoggedInUser_shouldRenderTemplate(self):
        self.create_recipe()
        self.client.force_login(self.user)
        response = self.client.get(reverse('details-recipe', args=(self.recipe.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'recipes/details.html')

    def test_detailsRecipeGet_shouldShowAllDetails(self):
        self.create_recipe()
        self.create_like()
        self.create_comment()
        self.client.force_login(self.user)
        response = self.client.get(reverse('details-recipe', args=(self.recipe.pk,)))
        ingredients = response.context.get('ingredients')
        comments = response.context.get('comments')
        is_owner = response.context.get('is_owner')
        is_liked = response.context.get('is_liked')
        self.assertIsNotNone(ingredients)
        self.assertIsNotNone(comments)
        self.assertIsNotNone(is_owner)
        self.assertIsNotNone(is_liked)

    def test_detailsRecipePost_shouldCreateChoice(self):
        self.create_recipe()
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('details-recipe', args=(self.recipe.pk,)),
            data={
                'recipe-pk': self.recipe.pk,
                'date': datetime.date.today()
            }
        )
        user_choices_count = self.user.choice_set.count()
        self.assertRedirects(response, reverse('home'))
        self.assertNotEqual(0, user_choices_count)


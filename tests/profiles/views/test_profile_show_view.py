from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class ProfileShowViewTest(MainTestCase):
    def test_profileShow_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        response = self.client.get(reverse('show-profile', args=(self.user.id,)))
        self.assertRedirects(response, f'/auth/sign-in/?next=/profile/show/{self.user.id}')


    def test_profileShow_whenLoggedIn_shouldRenderTemplate(self):
        self.create_recipe()
        self.create_new_user()
        self.client.force_login(self.new_user)
        response = self.client.get(reverse('show-profile', args=(self.user.id,)))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profiles/show-profile.html')

    def test_profileShow_whenLoggedIn_shouldShowRecipes(self):
        self.create_recipe()
        self.create_new_user()
        self.client.force_login(self.new_user)
        response = self.client.get(reverse('show-profile', args=(self.user.id,)))
        recipes = response.context.get('object_list')
        recipes_count = recipes.count()
        recipe_title = recipes[0].title
        self.assertEqual(1, recipes_count)
        self.assertEqual(recipe_title, self.recipe.title)

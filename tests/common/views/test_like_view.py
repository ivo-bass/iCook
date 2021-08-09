from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class LikeRecipeViewTest(MainTestCase):
    def test_like_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.post(
            reverse('like-recipe', args=(self.recipe.pk,)),
            data={'recipe_pk': self.recipe.pk, 'text': 'test text'}
        )
        self.assertRedirects(response, '/auth/sign-in/?next=/like/1')

    def test_like_whenLoggedIn_shouldAddLikeAndRedirectToDetails(self):
        self.client.force_login(self.user)
        self.create_recipe()
        old_count = self.recipe.likes_count
        response = self.client.post(
            reverse('like-recipe', args=(self.recipe.pk,)),
        )
        new_count = self.recipe.likes_count
        self.assertNotEqual(old_count, new_count)
        self.assertEqual(1, new_count)
        self.assertRedirects(response, '/recipe/details/1')

    def test_like_whenLoggedInAndLiked_shouldDeleteLikeAndRedirectToDetails(self):
        self.client.force_login(self.user)
        self.create_recipe()
        self.create_like()
        old_count = self.recipe.likes_count
        response = self.client.post(
            reverse('like-recipe', args=(self.recipe.pk,)),
        )
        new_count = self.recipe.likes_count
        self.assertNotEqual(old_count, new_count)
        self.assertEqual(0, new_count)
        self.assertRedirects(response, '/recipe/details/1')

    # empty text for comment is invalid but the frontend handles it with client-side error

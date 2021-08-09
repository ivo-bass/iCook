from django.urls import reverse

from tests.base.main_test_case import MainTestCase


class CommentRecipeViewTest(MainTestCase):
    def test_comment_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        response = self.client.post(
            reverse('comment-recipe', args=(self.recipe.pk,)),
            data={'recipe_pk': self.recipe.pk, 'text': 'test text'}
        )
        self.assertRedirects(response, '/auth/sign-in/?next=/comment/1')

    def test_comment_whenLoggedIn_shouldAddCommentRedirectToDetails(self):
        self.client.force_login(self.user)
        self.create_recipe()
        old_count = self.recipe.comments_count
        response = self.client.post(
            reverse('comment-recipe', args=(self.recipe.pk,)),
            data={'recipe_pk': self.recipe.pk, 'text': 'test text'}
        )
        new_count = self.recipe.comments_count
        self.assertNotEqual(old_count, new_count)
        self.assertRedirects(response, '/recipe/details/1')

    # empty text for comment is invalid but the frontend handles it with client-side error

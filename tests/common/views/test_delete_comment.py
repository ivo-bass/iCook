from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.base.main_test_case import MainTestCase


UserModel = get_user_model()


class DeleteCommentViewTest(MainTestCase):

    def test_deleteComment_whenNotLoggedIn_shouldRedirectToSignInWithNext(self):
        self.create_recipe()
        self.create_comment()
        response = self.client.post(
            reverse('delete-comment', args=(self.recipe.pk, self.comment.pk))
        )
        self.assertRedirects(response, f'/auth/sign-in/?next=/delete-comment/{self.recipe.pk}/{self.comment.pk}')

    def test_deleteComment_whenUserIsOwner_shouldDeleteComment(self):
        self.create_recipe()
        self.create_comment()
        self.client.force_login(self.user)
        old_comment_set_count = self.recipe.comment_set.count()
        response = self.client.post(
            reverse('delete-comment', args=(self.recipe.pk, self.comment.pk))
        )
        new_comment_set_count = self.recipe.comment_set.count()
        self.assertNotEqual(old_comment_set_count, new_comment_set_count)
        self.assertRedirects(response, f'/recipe/details/{self.recipe.pk}')

    def test_deleteComment_whenUserIsNotOwner_shouldNotDeleteComment(self):
        self.create_recipe()
        self.create_comment()
        new_user = UserModel.objects.create_user(
            email='new@new.new',
            password=MainTestCase.PASSWORD,
        )
        new_user.is_active = True
        new_user.save()
        self.client.force_login(new_user)
        old_comment_set_count = self.recipe.comment_set.count()
        response = self.client.post(
            reverse('delete-comment', args=(self.recipe.pk, self.comment.pk))
        )
        new_comment_set_count = self.recipe.comment_set.count()
        self.assertEqual(old_comment_set_count, new_comment_set_count)
        self.assertRedirects(response, f'/recipe/details/{self.recipe.pk}')
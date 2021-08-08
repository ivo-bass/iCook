from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


UserModel = get_user_model()


class DeleteUserViewTest(TestCase):
    EMAIL = 'test@test.test'
    PASSWORD = 'qwe987qwe987'

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email=self.EMAIL,
            password=self.PASSWORD,
        )
        self.user.is_active = True
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_deleteUser_whenUserIsNotLoggedIn_shouldRedirectToSignIn(self):
        response = self.client.post(reverse('delete-user', args=(self.user.id, )))
        self.assertEqual(302, response.status_code)
        self.assertEqual('/auth/sign-in/?next=/auth/delete/1', response.headers['location'])

    def test_deleteUserSuccess_shouldDeleteUserAndRedirectToIndex(self):
        self.client.login(username=self.EMAIL, password=self.PASSWORD)
        response = self.client.post(reverse('delete-user', args=(self.user.id, )))
        user = UserModel.objects.first()
        self.assertIsNone(user)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('index'), response.headers['location'])


    def test_deleteUserCancel_shouldRedirectToUpdateProfile(self):
        self.client.login(username=self.EMAIL, password=self.PASSWORD)
        response = self.client.post(reverse('delete-user', args=(self.user.id, )), data={'cancel': 'cancel'})
        user = UserModel.objects.first()
        self.assertIsNotNone(user)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('update-profile'), response.headers['location'])
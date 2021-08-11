from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

from LetsCook.auth_icook.forms import SignUpForm, UserUpdateForm
from LetsCook.profiles.forms import ProfileUpdateForm
from tests.base.main_test_case import MainTestCase


class ProfileAdnUserUpdateViewTest(MainTestCase):
    def test_profileAdnUserUpdate_shouldRenderTemplateAndForms(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('update-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profiles/update-profile.html')
        self.assertIsInstance(response.context.get('u_form'), UserUpdateForm)
        self.assertIsInstance(response.context.get('p_form'), ProfileUpdateForm)

    def test_profileAdnUserUpdate_whenFormsValid_shouldUpdate(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('update-profile'),
            data={
                'email': 'new_email@new.new',
                'username': 'new_username',
                'first_name': 'new',
                'last_name': 'new',
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(['username', 'first_name', 'last_name'], response.context.get('p_form').changed_data)
        self.assertEqual(['email'], response.context.get('u_form').changed_data)

    def test_profileAdnUserUpdate_whenFormInvalid_shouldHaveErrors(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('update-profile'),
            data={
                'email': 'invalid email',
            },
        )
        is_valid = response.context.get('u_form').is_valid()
        self.assertFalse(is_valid)
        errors = response.context.get('u_form').errors.get('email')
        self.assertIn('Enter a valid email address.', errors)
        is_valid = response.context.get('p_form').is_valid()
        self.assertFalse(is_valid)
        errors = response.context.get('p_form').errors.get('username')
        self.assertIn('This field is required.', errors)

    # Todo: image upload test


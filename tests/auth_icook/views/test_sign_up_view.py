from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import mail

from LetsCook.auth_icook.forms import SignUpForm
from tests.base.main_test_case import MainTestCase


class SignUpViewTest(TestCase):
    def test_getSignUp_shouldRenderTemplateAndForm(self):
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='auth/sign-up.html')
        self.assertIsInstance(response.context_data['form'], SignUpForm)

    def test_signUp_whenFormValid_shouldCreateInactiveUser(self):
        response = self.client.post(reverse('sign-up'),
                                    data={
                                        'email': MainTestCase.EMAIL,
                                        'password1': MainTestCase.PASSWORD,
                                        'password2': MainTestCase.PASSWORD,
                                    },
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.first()
        self.assertFalse(user.is_active)

    def test_signUp_whenFormValid_shouldSendActivationEmail(self):
        self.client.post(reverse('sign-up'), data={
            'email': MainTestCase.EMAIL,
            'password1': MainTestCase.PASSWORD,
            'password2': MainTestCase.PASSWORD,
        })
        recipients = mail.outbox[0].recipients()
        self.assertIn(MainTestCase.EMAIL, recipients)

    def test_signUp_whenFormValid_shouldRenderActivationNeededHtml(self):
        response = self.client.post(reverse('sign-up'), data={
            'email': MainTestCase.EMAIL,
            'password1': MainTestCase.PASSWORD,
            'password2': MainTestCase.PASSWORD,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='auth/activation_needed.html')

    def test_signUp_whenWrongPassword2_shouldReturnFormInvalid(self):
        response = self.client.post(reverse('sign-up'), data={
            'email': MainTestCase.EMAIL,
            'password1': MainTestCase.PASSWORD,
            'password2': 'wrong pass2',
        })
        is_valid = response.context_data['form'].is_valid()
        self.assertFalse(is_valid)
        errors = response.context_data['form'].errors['password2']
        self.assertIn('The two password fields didn’t match.', errors)

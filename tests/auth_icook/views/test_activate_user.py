import re

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, int_to_base36

from LetsCook.auth_icook.views import activate


class ActivateUserTest(TestCase):
    def setUp(self):
        self.email = 'test@test.test'
        self.password = 'qwe987qwe987'

    def test_activationSuccess(self):
        self.client.post(reverse('sign-up'), data={
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        })

        user = auth.get_user(self.client)

        # Get token from email
        """
        
    Hi test,

    Welcome to iCook!

    Creating a profile you are able to add content to the website,
    to comment, like and more.

    Please click on the link to confirm your registration,
    http://testserver/auth/activate/MQ/ar30vl-3d4bb0d6069981fd617a854d24b2b60e/

    If you think, it's not you, then just ignore this email.
"""
        token_regex = r"activate/MQ\/([A-Za-z0-9:\-]+)\/"
        # email_content = mail.outbox[0].body
        # match = re.search(token_regex, email_content)
        # token = match.group(1)

        # user_id = get_user_model().objects.first().id
        # uidb64 = int_to_base36(user_id)
        # uidb64 = urlsafe_base64_encode(uidb64).encode()
        # # Verify
        # activate(self.client.request, uidb64, token)
        #
        # recipients = mail.outbox[0].body
        # self.assertIn(self.email, recipients)


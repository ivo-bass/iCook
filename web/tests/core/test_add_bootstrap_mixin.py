from django.forms import forms
from django.test import TestCase

from LetsCook.core.mixins import AddBootstrapFormControlMixin


class AddBootstrapFormControlMixinTest(TestCase):
    def test_addBootstrapToForm_addsClassToField(self):
        class TestForm(AddBootstrapFormControlMixin, forms.Form):
            test_field = forms.Field()

        form = TestForm()
        attrs = form.fields['test_field'].widget.attrs['class']
        self.assertIn('form-control', attrs)
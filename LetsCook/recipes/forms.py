from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, HTML, ButtonHolder, Submit
from django import forms
from django.forms import inlineformset_factory

from LetsCook.core.custom_layout_object import Formset
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.recipes.models import Recipe, Ingredient


class IngredientForm(AddBootstrapFormControlMixin, forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


# class RecipeForm(AddBootstrapFormControlMixin, forms.ModelForm):
#     class Meta:
#         model = Recipe
#         fields = '__all__'


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    fields=['name', 'quantity', 'measure'],
    extra=1,
    can_delete=True,
)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['created_by', ]

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('meal_type'),
                Field('image'),
                Field('description'),
                Field('time'),
                Field('servings'),
                Field('preparation'),
                Field('vegetarian'),
                Field('public'),
                Fieldset('Add ingredients',
                         Formset('ingredients')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

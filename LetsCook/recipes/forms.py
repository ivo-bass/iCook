import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, HTML, ButtonHolder, Submit, Column
from django import forms
from django.conf import settings
from django.forms import inlineformset_factory

from LetsCook.core.custom_layout_object import Formset
from LetsCook.core.delete_previos_image import delete_previous_image
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.recipes.models import Recipe, Ingredient


class IngredientForm(AddBootstrapFormControlMixin, forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    fields=['name', 'quantity', 'measure'],
    min_num=1,
    extra=0,
    can_delete=True,
    # widgets={
    #     'name': forms.TextInput(
    #         attrs={'class': 'create-field'}
    #     ),
    #     'quantity': forms.NumberInput(
    #         attrs={'class': 'create-field'}
    #     ),
    #     'measure': forms.Select(
    #         attrs={'class': 'create-field'}
    #     )
    # }
)


class Row(Div):
    css_class = "row d-flex flex-row justify-content-between align-items-bottom"
    pass


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author', )

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_group_wrapper_class = 'form-control'
        self.helper.help_text_inline = True
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Row(
                Column(Field('title')),
                Column(Field('meal_type'))
            ),
            HTML("<hr>"),
            Row(
                Column(Field('description')),
                Column(Field('image')),
            ),
            HTML("<hr>"),
            Row(
                Column(Field('time')),
                Column(Field('servings')),
            ),
            HTML("<hr>"),
            Row(
                Field('preparation'),
            ),
            HTML("<hr>"),
            Row(
                Fieldset('Add ingredients',
                         Formset('ingredients')),
            ),
            HTML("<hr>"),
            Row(
                Column(Field('vegetarian')),
                Column(Field('public')),
                Column(ButtonHolder(Submit('submit', 'save'))),
            ),

        )


class RecipeUpdateForm(forms.ModelForm):
    def save(self, commit=True):
        delete_previous_image(self, commit, model=Recipe, file_name='food-default.png')
        return super().save(commit=commit)

    class Meta:
        model = Recipe
        exclude = ('author', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_group_wrapper_class = 'form-control'
        self.helper.help_text_inline = True
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Row(
                Column(Field('title')),
                Column(Field('meal_type'))
            ),
            HTML("<hr>"),
            Row(
                Column(Field('description')),
                Column(Field('image')),
            ),
            HTML("<hr>"),
            Row(
                Column(Field('time')),
                Column(Field('servings')),
            ),
            HTML("<hr>"),
            Row(
                Field('preparation'),
            ),
            HTML("<hr>"),
            Row(
                Fieldset('Add ingredients',
                         Formset('ingredients')),
            ),
            HTML("<hr>"),
            Row(
                Column(Field('vegetarian')),
                Column(Field('public')),
                Column(ButtonHolder(Submit('submit', 'save'))),
            ),

        )
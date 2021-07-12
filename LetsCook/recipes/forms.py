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


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    fields=['name', 'quantity', 'measure'],
    min_num=1,
    extra=0,
    can_delete=True,
    widgets={
        'name': forms.TextInput(
            attrs={'class': 'create-field'}
        ),
        'quantity': forms.NumberInput(
            attrs={'class': 'create-field'}
        ),
        'measure': forms.Select(
            attrs={'class': 'create-field'}
        )
    }
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
        self.helper.field_class = 'col-md-9 create-field'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('meal_type'),
                Field('image'),
                Field('description'),
                Field('time'),
                Field('servings'),
                Field('preparation'),
                HTML("<br>"),
                Field('vegetarian'),
                Field('public'),
                HTML("<hr>"),
                HTML("<br>"),
                Fieldset('Add ingredients',
                         Formset('ingredients')),
                HTML("<hr>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

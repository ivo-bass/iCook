from cloudinary.forms import CloudinaryJsFileField, CloudinaryFileField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, HTML, ButtonHolder, Submit, Column
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from LetsCook.core.constants import VALID_IMAGE_EXTENSIONS
from LetsCook.core.custom_layout_object import Formset
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.core.utils import delete_previous_image
from LetsCook.recipes.models import Recipe, Ingredient


class IngredientForm(AddBootstrapFormControlMixin, forms.ModelForm):
    """
    Create and update ingredient form
    """
    class Meta:
        model = Ingredient
        fields = '__all__'

    def clean_quantity(self):
        """
        Sets the quantity value to 0 if not provided
        """
        quantity = self.cleaned_data['quantity']
        if not quantity:
            quantity = 0
        return quantity

    def clean_measure(self):
        """
        Sets the measure value to empty string if not provided
        """
        measure = self.cleaned_data['measure']
        if not measure:
            measure = ''
        return measure


# inline formset creation
IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    fields=['name', 'quantity', 'measure'],
    min_num=1,
    extra=0,
    can_delete=True,
)


class Row(Div):
    """
    Inherits layout div class and
    Adds css class 'row' to its
    """
    css_class = "row"


class RecipeForm(forms.ModelForm):
    """
    This is recipe creation form that allows adding the ingredients formset
    and setting the Cloudinary field to crop and store the image file
    """
    class Meta:
        model = Recipe
        exclude = ('author', 'recipe_views',)

    image = CloudinaryFileField(
        required=False,
        options={
            'crop': 'fill',
            'gravity': 'center',
            'width': 580,
            'height': 326,
            'folder': 'recipes',
        },
    )

    def __init__(self, *args, **kwargs):
        """
        Recipe html layout including ingredients formset layout
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_group_wrapper_class = 'form-control'
        self.helper.help_text_inline = True
        self.helper.error_text_inline = True
        self.fields['description'].help_text = "Short description"
        self.fields['image'].help_text = ".jpg, .jpeg, .png"
        self.fields['time'].help_text = "Total time in minutes"
        self.fields['servings'].help_text = "Servings number"
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


class RecipeUpdateForm(RecipeForm):
    """
    Inherits the RecipeForm and extends save method
    to delete previous image if exists
    """
    def save(self, commit=True):
        delete_previous_image(self, Recipe)
        return super().save(commit=commit)

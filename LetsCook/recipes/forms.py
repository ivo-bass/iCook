from django import forms
from django.forms import inlineformset_factory

from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.recipes.models import Recipe, Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, extra=10, max_num=10, fields='__all__')


class RecipeForm(AddBootstrapFormControlMixin, forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

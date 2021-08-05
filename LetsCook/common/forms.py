from django import forms

from LetsCook.common.models import Comment
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.recipes.models import Recipe


class CommentForm(AddBootstrapFormControlMixin, forms.ModelForm):
    """
    Form for creating a comment. Relates the comment to a recipe object
    """
    recipe_pk = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Comment
        fields = ('text', 'recipe_pk')

    def save(self, commit=True):
        """
        On save gets the recipe_pk from the view and
        assigns it to the comment
        """
        recipe_pk = self.cleaned_data['recipe_pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        comment = Comment(
            text=self.cleaned_data['text'],
            recipe=recipe,
        )

        if commit:
            comment.save()

        return comment

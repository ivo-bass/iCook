from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView

from LetsCook.common.forms import CommentForm
from LetsCook.common.models import Like
from LetsCook.recipes.models import Recipe


class IndexView(TemplateView):
    model = Recipe
    template_name = 'common/index.html'


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched'].lower()
        in_title = Recipe.objects.filter(
            title__icontains=searched,
            public=True,
        )
        in_description = Recipe.objects.filter(
            description__icontains=searched,
            public=True,
        )
        in_ingredients = Recipe.objects.filter(
            ingredient__name__icontains=searched,
            public=True,
        )
        recipes = set(in_title | in_description | in_ingredients)
        context = {
            'searched': searched,
            'recipes': recipes,
        }
        return render(request, 'recipes/search.html', context)
    return render(request, 'recipes/search.html')


# class CommentView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'


@login_required
def comment_recipe(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('details-recipe', pk)


@login_required
def like_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    like_object_by_user = recipe.like_set.filter(user_id=request.user.id).first()
    if like_object_by_user:
        like_object_by_user.delete()
    else:
        like = Like(
            recipe=recipe,
            user=request.user,
        )
        like.save()
    return redirect('details-recipe', recipe.pk)
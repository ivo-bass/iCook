from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from LetsCook.common.forms import CommentForm
from LetsCook.common.models import Like, Comment
from LetsCook.core.get_search_results import get_search_results
from LetsCook.recipes.models import Recipe


class IndexView(TemplateView):
    model = Recipe
    template_name = 'common/index.html'


def search(request):
    context = {}
    if request.method == 'POST':
        context = get_search_results(request)
    return render(request, 'common/search.html', context)


@login_required(login_url=reverse_lazy('sign-in'))
def comment_recipe(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('details-recipe', pk)


@login_required(login_url=reverse_lazy('sign-in'))
def delete_comment(request, recipe_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.id == comment.user.id:
        comment.delete()
    return redirect('details-recipe', recipe_pk)


@login_required(login_url=reverse_lazy('sign-in'))
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
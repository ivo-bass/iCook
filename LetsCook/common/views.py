from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from LetsCook.common.forms import CommentForm
from LetsCook.common.models import Like, Comment
from LetsCook.core.utils import get_top_recipes, get_search_results
from LetsCook.recipes.models import Recipe


def index(request):
    """
    Renders index page with the top recipes as a context
    login is not required
    :param request: get method only
    :return: index.html
    """
    try:
        most_views, most_likes, most_comments = get_top_recipes()
    except Exception as exc:
        print(exc)
        most_views, most_likes, most_comments = None, None, None
    context = {
        'most_views': most_views,
        'most_likes': most_likes,
        'most_comments': most_comments,
    }
    return render(request, 'common/index.html', context)


def search(request):
    """
    Search page view which has own search field with post request
    and also renders the results from navbar searches
    """
    context = {}
    if request.method == 'POST':
        context = get_search_results(request)
    return render(request, 'common/search.html', context)


@login_required(login_url=reverse_lazy('sign-in'))
def comment_recipe(request, pk):
    """
    This view does not render a template but saves the comment
    Relates the comment to the user and the recipe.
    If the form is invalid redirects to details view
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
    return redirect('details-recipe', pk)


@login_required(login_url=reverse_lazy('sign-in'))
def delete_comment(request, recipe_pk, comment_pk):
    """
    On success deletes the comment with the given pk.
    Ensures that user is able to delete only their own comments.
    """
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.id == comment.user.id:
        comment.delete()
    return redirect('details-recipe', recipe_pk)


@login_required(login_url=reverse_lazy('sign-in'))
def like_recipe(request, pk):
    """
    If the user has a like on the given recipe deletes it
    otherwise creates a new like
    """
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
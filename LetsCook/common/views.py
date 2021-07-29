from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from LetsCook.common.forms import CommentForm
from LetsCook.common.models import Like, Comment
from LetsCook.recipes.models import Recipe


class IndexView(TemplateView):
    model = Recipe
    template_name = 'common/index.html'


def perform_search(request):
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
    return context


def search(request):
    context = {}
    if request.method == 'POST':
        context = perform_search(request)
    return render(request, 'recipes/search.html', context)


# class SearchView(ListView):
#     model = Recipe
#     template_name = 'recipes/search.html'
#     paginate_by = 3
#
#
#     def get(self, request, *args, **kwargs):
#         super().get(self, request, *args, **kwargs)
#         return render(request, 'recipes/search.html')
#
#     def get_queryset(self):
#         context = perform_search(self.request)
#         return context['recipes']
#
#     # @staticmethod
#     def post(self, request):
#         context = perform_search(request)
#         return render(request, 'recipes/search.html', context)




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
from LetsCook.recipes.models import Recipe


def get_search_results(request):
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
from LetsCook.recipes.models import Recipe


def get_recipes_for_day(request, day):
    user = request.user
    choices_for_day = user.choice_set.filter(date=day)
    recipes = []
    if choices_for_day:
        recipes = [ch.recipe for ch in choices_for_day]
    return recipes


def get_top_recipes(request):
    all_public_recipes = Recipe.objects.filter(public=True)
    most_views = Recipe.objects.filter(public=True).order_by('recipe_views').last()
    most_likes = list(sorted(all_public_recipes, key=lambda obj: -obj.likes_count))[0]
    most_comments = list(sorted(all_public_recipes, key=lambda obj: -obj.comments_count))[0]
    return most_views, most_likes, most_comments
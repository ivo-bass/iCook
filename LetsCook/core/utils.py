import datetime
import os

from django.conf import settings

from LetsCook.profiles.models import Choice
from LetsCook.recipes.models import Recipe


def get_recipes_for_day(request, day):
    user = request.user
    choices_for_day = user.choice_set.filter(date=day)
    recipes = []
    if choices_for_day:
        recipes = [ch.recipe for ch in choices_for_day]
    return recipes


def get_recipes_for_current_days(request):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    recipes_today = get_recipes_for_day(request, today)
    recipes_yesterday = get_recipes_for_day(request, yesterday)
    recipes_tomorrow = get_recipes_for_day(request, tomorrow)
    return recipes_today, recipes_yesterday, recipes_tomorrow


def get_top_recipes():
    all_public_recipes = Recipe.objects.filter(public=True)
    most_views = Recipe.objects.filter(public=True).order_by('recipe_views').last()
    most_likes = list(sorted(all_public_recipes, key=lambda obj: -obj.likes_count))[0]
    most_comments = list(sorted(all_public_recipes, key=lambda obj: -obj.comments_count))[0]
    return most_views, most_likes, most_comments


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


def delete_previous_image(self, commit, model, default_file_name):
    db_profile = model.objects.get(pk=self.instance.pk)
    new_image = self.files.get('image')
    old_image = str(db_profile.image)
    old_image_path = os.path.join(settings.MEDIA_ROOT, old_image)
    if commit and new_image and old_image and not old_image == default_file_name:
        os.remove(old_image_path)


def save_suggestion(request):
    recipe_pk = request.POST.get('recipe-pk')
    recipe = Recipe.objects.get(pk=recipe_pk)
    user = request.user
    choice_made = Choice(
        recipe=recipe,
        user=user,
    )
    if request.POST.get('date'):
        choice_made.date = request.POST.get('date')
    choice_made.save()
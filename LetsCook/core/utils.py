import datetime

from cloudinary import uploader

from LetsCook.profiles.models import Choice
from LetsCook.recipes.models import Recipe


def get_recipes_for_day(request, day):
    """
    Filters the choices of the user by date
    and returns the recipes chosen for that day
    :param day: datetime instance
    :return: list of recipes
    """
    user = request.user
    choices_for_day = user.choice_set.filter(date=day)
    recipes = []
    if choices_for_day:
        recipes = [ch.recipe for ch in choices_for_day]
    return recipes


def get_recipes_for_current_days(request):
    """
    Returns the chosen recipes for yesterday, today and tomorrow
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    recipes_today = get_recipes_for_day(request, today)
    recipes_yesterday = get_recipes_for_day(request, yesterday)
    recipes_tomorrow = get_recipes_for_day(request, tomorrow)
    return recipes_today, recipes_yesterday, recipes_tomorrow


def get_top_recipes():
    """
    Filters recipes by likes count, comments count
    and views count than returns the top recipes
    """
    all_public_recipes = Recipe.objects.filter(public=True)
    most_views = Recipe.objects.filter(public=True).order_by('recipe_views').last()
    most_likes = list(sorted(all_public_recipes, key=lambda obj: -obj.likes_count))[0]
    most_comments = list(sorted(all_public_recipes, key=lambda obj: -obj.comments_count))[0]
    return most_views, most_likes, most_comments


def get_search_results(request):
    """
    Performs search using a keyword case insensitive in
    title, description and ingredients fields and returns set union
    """
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


def delete_previous_image(self, model):
    """
    Deletes the old image from cloudinary database
    after uploading a new one
    """
    db_profile = model.objects.get(pk=self.instance.pk)
    new_image = self.files.get('image')
    if new_image:
        try:
            old_image = db_profile.image.public_id
            uploader.destroy(old_image)
        except Exception as exc:
            print(exc)


def save_suggestion(request):
    """
    Takes the request and saves the choice of recipe
    with the given date for the current user
    """
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
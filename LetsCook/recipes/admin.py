from django.contrib import admin

from LetsCook.recipes.models import Recipe, Ingredient


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Recipe views should not be changed
    With inlines the ingredients are displayed
    """
    list_display = ('title', 'created_on', 'public', 'author')
    inlines = [IngredientInlineAdmin, ]
    readonly_fields = ('recipe_views',)

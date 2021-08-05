from django.contrib import admin

from LetsCook.recipes.models import Recipe, Ingredient


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Author field should not be changed
    """
    list_display = ('title', 'created_on', 'public', 'author')
    inlines = [IngredientInlineAdmin, ]
    readonly_fields = ('author', 'recipe_views')

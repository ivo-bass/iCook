from django.contrib import admin

from LetsCook.recipes.models import Recipe, Ingredient


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'ingredients', 'upload_time', 'public']
    inlines = [IngredientInlineAdmin, ]

from django.contrib import admin

from LetsCook.recipes.models import Recipe, Ingredient, MealType


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'ingredients', 'created_on', 'public']
    inlines = [IngredientInlineAdmin, ]


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    pass
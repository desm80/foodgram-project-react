from django.contrib import admin

from .models import Tag, Ingredient, Recipe, RecipeIngredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображение модели Tag в Админке."""

    list_display = (
        'pk',
        'name',
        'color',
        'slug',

    )
    list_editable = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Отображение модели Ingredient в Админке."""

    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    # min_num = 1
    # extra = 1


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('id', 'recipe', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Отображение модели Recipe в Админке."""

    list_display = (
        'pk',
        'name',
        'author',
    )
    list_editable = (
        'name',
    )
    list_filter = (
        'author',
        'tags',
    )
    search_fields = (
        'name',
    )
    inlines = (RecipeIngredientsInline,)
    empty_value_display = '-пусто-'


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
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient


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
        'get_favorites',
    )
    list_editable = (
        'name',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    search_fields = (
        'name',
    )
    inlines = (RecipeIngredientsInline,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(RecipeAdmin, self).formfield_for_dbfield(
            db_field, **kwargs
        )
        if db_field.name == "author":
            field.initial = kwargs["request"].user.id
        return field

    def get_favorites(self, obj):
        return obj.favorites.count()

    get_favorites.short_description = (
        'Число добавлений этого рецепта в избранное'
    )
    empty_value_display = '-пусто-'


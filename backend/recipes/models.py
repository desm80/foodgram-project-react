from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    color = ColorField(
        unique=True,
        max_length=7,
        verbose_name='Цвет в HEX',
        blank=True,
        null=True,
        default='#FFFFE0'
        )
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'color'],
                name='unique_tag')
        ]

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=False,
        )
    text = models.TextField()
    cooking_time = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        ordering = ('-id',)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_recipe_ingredient',
            ),
        )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        ]

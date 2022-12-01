from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(
        max_length=7,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex='^#(?:[0-9a-fA-F]{1,2}){3}$',
                message='HEX color required')
        ],
    )
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'color'],
                name='unique_tag')
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient')
        ]


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
    cooking_time = models.SmallIntegerField(validators=[
        MinValueValidator(1),
    ])


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(validators=[
        MinValueValidator(1),
    ])

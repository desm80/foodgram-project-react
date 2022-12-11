import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from rest_framework import serializers, exceptions


from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient, Favorite, \
    ShoppingCart
from users.serializers import MyUserSerializer

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class FavoriteShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[MinValueValidator(
            1,
            message='Количество должно быть равным или больше 1!'
            )
        ]
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipePostUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientForRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'author', 'image', 'name',
                  'text', 'cooking_time')

    def validate(self, data):
        cooking_time = data['cooking_time']
        ingredients = data['ingredients']
        tags = data['tags']
        if cooking_time <= 0:
            raise exceptions.ValidationError(
                'Время приготовления должно быть больше нуля!'
            )
        if len(ingredients) == 0:
            raise exceptions.ValidationError(
                'В рецепт не добавлены ингредиенты'
            )
        if len(ingredients) != len(set([item['id'] for item in ingredients])):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться!')
        ingredients = data['ingredients']
        for ingredient in ingredients:
            if not Ingredient.objects.filter(
                    id=ingredient['id']).exists():
                raise serializers.ValidationError({
                    'ingredients': f'Ингредиента с id - {ingredient["id"]} '
                                   f'нет в базе'
                })
        if len(tags) != len(set([item for item in tags])):
            raise serializers.ValidationError({
                'tags': 'Тэги не должны повторяться!'})

        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()

        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'], )
            for ingredient in ingredients
        ])
        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.save()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for tag in tags:
            instance.tags.add(tag)
            instance.save()

        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=instance,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'], )
            for ingredient in ingredients
        ])

        return instance

    def to_representation(self, value):
        serializer = RecipeSerializer(value, context=self.context)
        return serializer.data

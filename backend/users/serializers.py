from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class MyUserSerializer(UserSerializer):
    """Сериализатор для эндпоита users."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        # lookup_field = 'username'

    def get_is_subscribed(self, obj):
        """Подписан ли пользователь на автора."""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели User."""
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для короткой модели рецепта в подписках."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
#
#
# class FollowSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField(read_only=True)
#     recipes = serializers.SerializerMethodField(read_only=True)
#     recipes_count = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count',
#         )
#         read_only_fields = ('email', 'username', 'first_name', 'last_name',)
#
#     def get_is_subscribed(self, obj):
#         user = self.context.get('request').user
#         if not user:
#             return False
#         return Follow.objects.filter(user=user, author=obj).exists()
#
#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         limit_recipes = request.query_params.get('recipes_limit')
#         if limit_recipes is not None:
#             recipes = obj.recipes.all()[:(int(limit_recipes))]
#         else:
#             recipes = obj.recipes.all()
#         context = {'request': request}
#         return FollowRecipeSerializer(recipes, many=True,
#                                       context=context).data
#
#     def get_recipes_count(self, obj):
#         return obj.recipes.count()


class FollowSerializer(MyUserSerializer):
    """
    Сериализатор для вывода подписок пользователя
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return FollowRecipeSerializer(recipes, many=True).data

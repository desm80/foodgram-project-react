from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from api.filters import IngredientFilter, RecipeFilter
from api.serializers import (FavoriteShoppingSerializer, IngredientSerializer,
                             RecipePostUpdateSerializer, RecipeSerializer,
                             TagSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Описание логики работы АПИ для эндпоинта Tag."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    # lookup_field = 'slug'


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Описание логики работы АПИ для эндпоинта Ingredient."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    # filter_backends = (IngredientFilter,)
    # search_fields = ('^name',)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Описание логики работы АПИ для эндпоинта Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    #  IsAdminAuthorOrReadOnly, IsAuthenticatedOrReadOnly
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Получение сериализатора для работы с Рецептами."""

        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipePostUpdateSerializer

    def perform_create(self, serializer):
        """Подстановка текущего пользователя в авторы рецепта."""
        serializer.save(author=self.request.user)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['GET']
            )
    def download_shopping_cart(self, request):
        """Обработка скачивания списка Покупок."""

        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(ingredient_total=Sum('amount'))
        content = ''
        for ingredient in ingredients:
            content += (
                f'∙ {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}) '
                f'- {ingredient["ingredient_total"]}\n'
            )
        filename = "shopping_cart.txt"
        response = HttpResponse(
            content, content_type='text/plain', charset='utf-8'
        )
        response['Content-Disposition'] = \
            'attachment; filename={0}'.format(filename)
        return response


class FavoriteAPIView(APIView):
    """Описание логики работы АПИ для эндпоинта Favorite."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Добавление рецепта в Избранное."""
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(
                user=request.user,
                recipe_id=recipe_id
        ).exists():
            return Response(
                {'error': 'Рецепт уже добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response(
            FavoriteShoppingSerializer(
                recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Удаление рецепта из Избранного."""
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Рецепта нет в вашем списке избранного'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartAPIView(APIView):
    """Описание логики работы АПИ для эндпоинта ShoppingCart."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Добавление рецепта в список Покупок."""
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingCart.objects.filter(
                user=request.user,
                recipe_id=recipe_id
        ).exists():
            return Response(
                {'error': 'Рецепт уже добавлен в список покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        return Response(
            FavoriteShoppingSerializer(
                recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Удаление рецепта из списка Покупок."""
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        cart = ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if cart:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Рецепта нет в вашем списке покупок'},
            status=status.HTTP_400_BAD_REQUEST
        )

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TagSerializer, IngredientSerializer, \
    RecipeSerializer, FavoriteShoppingSerializer, RecipePostUpdateSerializer
from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, \
    RecipeIngredient


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Описание логики работы АПИ для эндпоинта Tag."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    lookup_field = 'slug'


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Описание логики работы АПИ для эндпоинта Ingredient."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Описание логики работы АПИ для эндпоинта Recipe."""
    # serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipePostUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated],
            methods=['GET']
            )
    def download_shopping_cart(self, request):

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

    def post(self, request,  *args, **kwargs):
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

    def post(self, request,  *args, **kwargs):
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

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView

from api.serializers import TagSerializer, IngredientSerializer, \
    RecipeSerializer, FavoriteSerializer
from recipes.models import Tag, Ingredient, Recipe, Favorite


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
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteAPIView(APIView):

    def post(self, request,  *args, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response(
            FavoriteSerializer(recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


    def delete(self, request, *args, **kwargs):
        ...



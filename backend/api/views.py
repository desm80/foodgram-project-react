from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.serializers import TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient


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



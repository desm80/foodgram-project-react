from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Переопределение стандартного PageNumberPagination для вывода
    лимитированного количества рецептов на страницу."""
    # page_size = 6
    page_size_query_param = 'limit'

from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class CustomPaginator(PageNumberPagination):
    # page_size = 6
    page_size_query_param = 'limit'

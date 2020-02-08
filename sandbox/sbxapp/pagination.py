from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class LimitOffsetPaginationWithMaxLimit(LimitOffsetPagination):
    max_limit = 10


class MyPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'per'
    max_page_size = 1000

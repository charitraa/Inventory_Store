from rest_framework.pagination import PageNumberPagination

class DEfaultPagination(PageNumberPagination):
    page_size = 10
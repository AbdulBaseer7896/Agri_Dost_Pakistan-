from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Default page size: 30
    Frontend can override with ?page_size=12|24|30|40|50|100 (max 100)
    """
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

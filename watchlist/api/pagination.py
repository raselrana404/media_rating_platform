from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination,
                                       CursorPagination,
                                       )


class WatchListPNPagination(PageNumberPagination):
    # If we use this, client side(user) can't modify page size.
    page_size = 5

    # page_query_param - A string value indicating the name of the query parameter to use for the pagination control. Default is 'page' -> [?page=number]
    # page_size_query_param = 'page'  # default
    # Overriding default parameter name (page)
    # page_query_param = 'p'

    # page_size_query_param - If set, this is a string value indicating the name of a query parameter that allows the client to set the page size on a per-request basis. Defaults to None, indicating that the client may not control the requested page size.
    # Here in this case, page size is 10, and user is able to set the page size using this size query parameter.
    page_size_query_param = 'size'

    # max_page_size - If set, this is a numeric value indicating the maximum allowable requested page size. This attribute is only valid if page_size_query_param is also set.
    max_page_size = 15

    # last_page_strings - A list or tuple of string values indicating values that may be used with the page_query_param to request the final page in the set. Defaults to ('last',)
    # last_page_strings = 'end'


class WatchListLOPagination(LimitOffsetPagination):
    # default_limit - A numeric value indicating the limit to use if one is not provided by the client in a query parameter. Defaults to the same value as the PAGE_SIZE settings key.
    default_limit = 5

    # max_limit - If set this is a numeric value indicating the maximum allowable limit that may be requested by the client. Defaults to None.
    max_limit = 10


class WatchListCPagination(CursorPagination):
    page_size = 5
    # ordering = This should be a string, or list of strings, indicating the field against which the cursor based pagination will be applied. For example: ordering = 'slug'. Defaults to -created. This value may also be overridden by using OrderingFilter on the view.
    ordering = 'created'

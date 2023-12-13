from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class QueryLoggingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Clear the old queries
        connection.queries.clear()

    def process_template_response(self, request, response):
        # Add the queries to the context
        response.context_data['sql_queries'] = connection.queries
        return response

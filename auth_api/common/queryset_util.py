from django.core.paginator import Paginator, EmptyPage

from common.generic.response import Response
from common.response import PageTypeResults


class QuerySetUtil:
    def pagination(
        self, results_set, page=1, size=20, order_by_filed="-creationTime", results=None, page_type_result=None
    ):
        queryset_list = results_set.order_by(order_by_filed)
        paginator = Paginator(queryset_list, per_page=size)

        try:
            queryset_list = paginator.page(page)
        except EmptyPage:
            queryset_list = paginator.page(1)

        if not results:
            results = Response()
            results.code = 200
        if not page_type_result:
            page_type_result = PageTypeResults()

        results.data = page_type_result
        page_type_result.page = page
        page_type_result.total = paginator.count
        page_type_result.size = len(queryset_list)
        page_type_result.total_page = paginator.num_pages

        return queryset_list, results

    def all_results(self, results_set, order_by_filed="-creationTime", results=None, page_type_result=None):
        queryset_list = results_set.order_by(order_by_filed)
        paginator = Paginator(queryset_list, per_page=100000)
        queryset_list = paginator.page(1)

        if not results:
            results = Response()
            results.code = 200
        if not page_type_result:
            page_type_result = PageTypeResults()
        results.data = page_type_result
        page_type_result.page = 1
        page_type_result.total = paginator.count
        page_type_result.size = len(queryset_list)
        page_type_result.total_page = paginator.num_pages
        return queryset_list, results


queryset_util = QuerySetUtil()

from django.core.paginator import Paginator, InvalidPage
from django.db.models import QuerySet
from django.views.generic.base import ContextMixin
from rest_framework.serializers import SerializerMetaclass

from django.db import models

from common_modules.exception.obj import ObjNOTFoundError


class SingleObjectMixin(ContextMixin):
    model = None
    queryset = None
    pk = None
    custom_pk_field = "slug"
    custom_pk_value = "slug"  # id pk identify

    pk_url = "pk"
    query_pk_and_slug = False
    context_object_name = None

    exclude = None
    fields = None

    kwargs: dict  # 获取URL的参数

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if self.pk is not None:
            queryset = queryset.filter(pk=self.pk)

        pk = self.kwargs.get(self.pk_url)
        custom_pk_value = self.kwargs.get(self.custom_pk_field)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if custom_pk_value is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.custom_pk_field
            queryset = queryset.filter(**{slug_field: custom_pk_value})

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise ObjNOTFoundError()
        return obj

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ValueError("缺失模型 无法查询")
        return self.queryset.all()

    def get_obj_name(self, obj):
        if isinstance(obj, models.Model):
            return obj._meta.model_name
        else:
            return None


class ParamsMixin:
    def _add_search_params(self, request, obj_list):
        """"""


class MultipleObjectMixin(ContextMixin, ParamsMixin):
    model = None
    ordering = ("creationTime",)
    queryset = None
    paginate_by = None
    allow_empty = True
    paginator_class = Paginator

    exclude = None
    fields = None
    page_kwargs = "page"
    size_kwargs = "size"
    paginate_orphans = 0  # 最后一页允许的最小项目数
    kwargs: dict
    object_list: queryset
    serializer: SerializerMetaclass = None
    partial = True

    def get_queryset(self):
        serializer = self.serializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        self.serializer = serializer
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            ValueError("缺失模型 无法查询")

        ordering = self.ordering
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        add_params = self._add_search_params(request=self.request, obj_list=queryset)
        if add_params is not None:
            queryset = add_params
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        super(MultipleObjectMixin, self).get_context_data(**kwargs)
        queryset = object_list if object_list is not None else self.object_list
        size_kwargs = self.size_kwargs
        size = self.serializer.validated_data.get(size_kwargs)
        size = int(size)

        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, size)
        context = {"paginator": paginator, "page_obj": page, "is_paginated": is_paginated, "object_list": queryset}
        self.object_list = queryset
        context.update(kwargs)
        return super(MultipleObjectMixin, self).get_context_data(**context)

    def paginate_queryset(self, queryset, size):
        paginator = self.get_paginator(queryset, size, allow_empty_first_page=self.allow_empty)
        page_kwargs = self.page_kwargs
        page = self.serializer.validated_data.get(page_kwargs)
        try:
            page_num = int(page)
        except Exception as e:
            page_num = 1
        try:
            page = paginator.page(page_num)
            return paginator, page, page.object_list, page.has_other_pages()
        except InvalidPage as e:
            return paginator, page, self.object_list, 0

    def get_paginator(self, queryset, size, orphans=0, allow_empty_first_page=True, **kwargs):
        return self.paginator_class(queryset, size, orphans=orphans, allow_empty_first_page=allow_empty_first_page)

    @property
    def get_paginate_by(self):
        return self.paginate_by

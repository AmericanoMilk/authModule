from functools import partial

from django.db import transaction
from django.views.generic.base import ContextMixin
from rest_framework.serializers import SerializerMetaclass
from common_modules.logger import logger


def on_commit_func(obj=None, *args, **kwargs):
    print(args, kwargs, obj)


class TransactionObject:
    def __enter__(self):
        with transaction.atomic():
            if hasattr(self, "obj"):
                transaction.on_commit(self.obj)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class EvolutionObjMixin(ContextMixin):
    model = None
    serializer: SerializerMetaclass = None

    def get_object(self, data):
        # 参数校验，并且构建data
        if isinstance(data, bytes):
            data: bytes = data.decode("UTF8")
        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.serializer = serializer

    def save(self, data):
        self.serializer.save(data)
        return data

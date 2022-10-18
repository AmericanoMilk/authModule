from typing import Iterable

from django.http import HttpRequest
from rest_framework.views import APIView

from common.generic.evolution import EvolutionObjMixin, TransactionObject
from common.generic.model import get_model_dict
from common.vail import parsed_calibration_params


class BasePOSTDetailEditorView(EvolutionObjMixin, APIView):
    @parsed_calibration_params
    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object(request.data)
        # 开启事物
        with TransactionObject() as aff:
            context = self.get_context_data(object=self.object)
            context["data"] = self._detail_handler_func(request=request, **context)
        return self.save(data=context['data'])

    def _detail_handler_func(self, request, object, view) -> dict:
        """
        业务处理
        :param request:
        :param object:
        :param view:
        :return:
        """
        return object

    def save_valid(self, data):
        for key, value in data:
            if isinstance(value, Iterable):
                return self.save_valid(data)

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context["object"] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)


class BasePUTDetailEditorView(APIView):
    pass


class BaseDELETEDetailEditorView(APIView):
    pass

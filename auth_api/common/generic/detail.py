from rest_framework.views import APIView

from auth_api.common.generic.model import get_model_dict
from auth_api.common.generic.obj import SingleObjectMixin


class BaseGETDetailView(SingleObjectMixin, APIView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['data'] = self._detail_handler_func(request=request, **context)
        return context

    def _detail_handler_func(self, request, object, view) -> dict:
        return get_model_dict(object, exclude=self.exclude, fields=self.fields)

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

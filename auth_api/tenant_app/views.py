from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from common.generic.response import Response
from common.obj.transaction import Transaction
from common.queryset_util import queryset_util
from common.response import Results
from common.account.token import token_util
from common.vail import parsed_calibration_params
from tenant_app.serializer import TenantLoginSerializer, TenantRegisterSerializer, TenantSearchSerializer
from tenant_app.utility.tenant_manager_helper import tenant_manger_helper


# Create your views here.


class TenantLoginView(APIView):
    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        response = Response()
        ser = TenantLoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        tenant, password = ser.validated_data.get("tenant"), ser.validated_data.get("password")

        _user = auth.authenticate(request=request, user=None, tenant=tenant, password=password)
        auth.login(request=request, user=_user)
        token = token_util.generate_token(instance=_user)
        token_util.upload_token(instance=_user, token=token)

        response.data = {
            "access_token": token,
            "tenantId": _user.uuid,
            "name": _user.name,
            "isAdmin": _user.is_admin,
            "isActive": _user.is_normal,
            "lastLogin": int(_user.last_login.timestamp())
        }
        return response


class TenantRegister(APIView):
    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        ser = TenantRegisterSerializer(data=request.data)
        response = Results()
        # 进入事务 直接无视错误
        with Transaction(response=response):
            ser.is_valid(raise_exception=True)
            validate_password(ser.validated_data['password'])
            ser.save()
        # 信息写到Redis

        response.msg = f"create {ser.instance.tenant} success"
        return response


class TenantInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (authentication.JWTAuthentication,)

    @parsed_calibration_params
    def get(self, request, *args, **kwargs):
        ser = TenantSearchSerializer(data=request.data)
        tenant = request.tenant

        be_search_tenant = ser.validated_data.get("tenant")
        all_results = ser.validated_data.get("all_results")
        page = ser.validated_data.get("page")
        size = ser.validated_data.get("size")

        tenant_list = tenant_manger_helper.search_tenant(tenant, be_search_tenant=be_search_tenant,
                                                         all_results=all_results)
        tenant_list, response = queryset_util.pagination(tenant_list, page=page, size=size)
        return response

    def update(self, request, *args, **kwargs):
        # password 修改后强制所有token过期
        pass

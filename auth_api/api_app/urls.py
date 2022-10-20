from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from api_app.views import TokenObtainPairIoTView, TokenRefreshIoTView, TokenVerifyIoTView

urlpatterns = [
    path('token', TokenObtainPairIoTView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshIoTView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyIoTView.as_view(), name='token_verify'),
    path('token/blacklist', TokenBlacklistView.as_view(), name='token_blacklist'),
]

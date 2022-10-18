from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.TenantLoginView.as_view()),
    path("register", views.TenantRegister.as_view()),
    path("tenants", views.TenantInfoView.as_view()),
]

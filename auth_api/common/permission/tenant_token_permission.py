from rest_framework.permissions import BasePermission


class TenantTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True

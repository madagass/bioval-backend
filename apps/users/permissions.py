from rest_framework.permissions import BasePermission


class IsAdminGlobal(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "admin_global")


class IsAdminMetier(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "admin_metier")


class IsAdminExterne(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "admin_externe")


class IsAnyAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.role in ["admin_global", "admin_metier", "admin_externe"]
        )


class IsAdminGlobalOrMetier(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.role in ["admin_global", "admin_metier"]
        )


class IsAdminGlobalOrExterne(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.role in ["admin_global", "admin_externe"]
        )
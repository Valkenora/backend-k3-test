from rest_framework.permissions import BasePermission


class IsForeman(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == 'foreman')


class IsSHEOfficer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == 'she_officer')


class IsSHECoordinator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == 'she_coordinator')


class IsSiteManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == 'site_manager')


class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == 'project_manager')


class IsSiteOrProjectManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ['site_manager', 'project_manager'])


class IsSHEOfficerOrCoordinator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ['she_officer', 'she_coordinator'])


class IsAnyRole(BasePermission):
    """Any authenticated user regardless of role — for read-only shared views"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
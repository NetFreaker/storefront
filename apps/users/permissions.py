# apps/users/permissions.py
from rest_framework import permissions

class IsServiceProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'service_provider'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

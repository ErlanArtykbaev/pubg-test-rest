from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsUsers(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff







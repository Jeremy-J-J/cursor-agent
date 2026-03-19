from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner or admin
        return obj == request.user or request.user.role == 'admin'


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderator users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'moderator']


class IsPremiumUser(permissions.BasePermission):
    """
    Custom permission to only allow premium users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'moderator', 'premium']
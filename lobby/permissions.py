from rest_framework import permissions

class IsObjectOwner(permissions.BasePermission):
    '''
    Permission is only given to authenticated users that own the object
    '''
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user.username

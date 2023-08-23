from rest_framework import permissions

class IsShopOwner(permissions.BasePermission):
    """
    Custom permission to only allow shop owners to view and edit.
    """

    def has_permission(self, request, view):
        # Check if the user is a shop owner.
        return request.user.userprofile.is_shop_owner

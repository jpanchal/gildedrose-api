from rest_framework.permissions import BasePermission
from .models import Itemlist


class IsOwner(BasePermission):
    """Custom permission class to allow itemlist owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the itemlist owner."""
        if isinstance(obj, Itemlist):
            return obj.owner == request.user
        return obj.owner == request.user

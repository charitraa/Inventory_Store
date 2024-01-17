
from rest_framework import permissions


class ISAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
class FullDjangoModelpermission(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view _%(model_name)s'],

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.has_perm('store.view_history')
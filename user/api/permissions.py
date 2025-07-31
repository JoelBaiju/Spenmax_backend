from rest_framework import permissions
from user.variable import ADMIN,USER,VENDOR
from datetime import datetime
from rest_framework.exceptions import PermissionDenied

class IsAdminUserType(permissions.BasePermission):
    """
    Custom permission to only allow users with 'Admin' user type to access the view.
    """

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        
        return request.user.user_type == ADMIN


class IsNotAdminType(permissions.BasePermission):
    """
    Custom permission to only allow users with 'Vendor' , "user"  user type to access the view or for the anonymous user only
    """
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return True
        
        return request.user.user_type != ADMIN
    
class IsUserType(permissions.BasePermission):

    def has_permission(self, request , view):

        if not request.user.is_authenticated:
            return False
        
        if request.user.user_type == USER:
            package_options = request.user.detail_c.package_c.filter(expiry_date__lte=datetime.today() , is_active = True)
            if package_options.exists():
                package_options.update(is_active=False)
            is_expired = request.user.detail_c.package_c.filter(expiry_date__gt=datetime.today() , is_active = True).exists()
            if not is_expired:
                raise PermissionDenied("Your package has expired.", code='package_expired')
            return is_expired
        return False
class IsUserType_u(permissions.BasePermission):

    def has_permission(self, request , view):

        if not request.user.is_authenticated:
            return False
        
        if request.user.user_type == USER:
            return True
        return False

class IsUserAndNoPackage(permissions.BasePermission):
    def has_permission(self, request , view):

        if not request.user.is_authenticated:
            return False
        
        if request.user.user_type == USER:
            package_options = request.user.detail_c.package_c.filter(expiry_date__lte=datetime.today() , is_active = True)
            if package_options.exists():
                package_options.update(is_active=False)
            is_expired = request.user.detail_c.package_c.filter(expiry_date__gt=datetime.today() , is_active = True).exists()
            if is_expired:
                raise PermissionDenied("you already have a package", code='package_expired')
            return not is_expired
        return False

class IsAdminOrVendor(permissions.BasePermission):

    def has_permission(self, request , view):

        if not request.user.is_authenticated:
            return False
        
        return request.user.user_type == VENDOR  or request.user.user_type == ADMIN
    
class IsVendorType(permissions.BasePermission):

    def has_permission(self, request , view):

        if not request.user.is_authenticated:
            return False
        
        return request.user.user_type == VENDOR

from app.models.user import User
from app.models.permission import Permission
from flask import abort

from app.services.user_service import UserService
 
class PermissionService():
    
    def check_permission(user_email,type_permission):
        user_permits = (UserService.find_by_email(user_email)).has_permission(Permission.find_by_name(type_permission))
        return True if user_permits else abort(401)
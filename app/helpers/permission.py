from app.models.user import User
from app.models.permission import Permission
from app.services.user_service import UserService

def check_permission(email,permission):
    user = UserService.find_by_email(email)
    permission = Permission.find_by_name(permission)
    return user.has_permission(permission)

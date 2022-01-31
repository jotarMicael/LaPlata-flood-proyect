from flask import session, abort
from app.helpers.auth import authenticated
from app.models.user import User
from app.db import db
from app.services.user_service import UserService
 

class AuthenticationService:

    def check_authentication():
        user = authenticated(session)
        return (user if user else abort(401))
    
    def update_active_role(parameters,user_email):
        user = UserService.find_by_email(user_email)
        user.active_role = parameters['active_role']
        db.session.commit()
        roles = {role.id: role.name for role in user.roles}
        actual_role = next(iter(roles))
        actual_role_aux = (user.active_role)
        session["actual_role"] = {actual_role:actual_role_aux}
        session["roles"]= roles
        session["actual_role"] = {actual_role:parameters['active_role']}
        return {'message': 'El rol activo fue modificado con exito!', 'category': 'success'}
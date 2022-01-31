from flask import abort
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.db import db
from sqlalchemy.sql import func
from sqlalchemy.sql import expression

class UserService():

    @classmethod
    def get_users(cls):
        query = db.session.query(User.id,User.first_name,User.last_name,User.username,User.email, User.active, expression.label('roles', func.group_concat(Role.name, ' '))).select_from(User)
        join_query = query.join(UserRole).join(Role)
        return join_query.filter(User.first_name.like('%'+''+'%'), UserRole.active == 1).group_by(User.id)

    @classmethod
    def find_by_email(cls,email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def find_by_email_and_pass(cls,email,password):
        return User.query.filter_by(email=email,password=password).first()
    
    def get_active():   
        return User.active

    @classmethod
    def get_user(cls,id):
        user = User.query.get(id)
        return user if user else abort(404)

    @classmethod
    def update_user(cls,parameters,roles):
        return UserService.modify_user(parameters,roles)
    
    @classmethod
    def modify_user(cls, parameters,roles):        
        user_to_update = cls.get_user(parameters["user_id"])
        if (parameters["password"]):
            user_to_update.password = parameters["password"]
        user_to_update.updated_at = func.now()
        
        db.session.commit()              
        return {'message': 'El usuario fue modificado con exito!', 'category': 'success'}


    @classmethod
    def destroy_user(cls, id):
        user_to_destroy = cls.get_user(id)
        user_to_destroy.active = 0
        db.session.commit()
        return {'message': 'El usuario fue inhabilitado con exito!', 'category': 'success'}

    @classmethod
    def reactivate_user(cls, id):
        user_to_reactivate = cls.get_user(id)
        user_to_reactivate.active = 1
        db.session.commit()
        return {'message': 'El usuario fue habilitado con exito!', 'category': 'success'}

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
    @staticmethod
    def create (users_name, users_email):
        user = User(first_name=users_name, email=users_email,last_name='google',username=users_email,active=0,active_role='operator')
        db.session.add(user) 
        db.session.flush()
        db.session.add(UserRole(role_id=2,user_id= user.id))
        db.session.commit()
        return True
    @staticmethod
    def get_active(email):  
        user = User.query.filter_by(email=email,active=1).first()
        return user if user else False


    @classmethod
    def json_users(cls):
        a = db.session.query(User.id,User.email,User.first_name, User.last_name, User.username).filter(
            User.active==1
        )
        return [ar._asdict() for ar in a] if  a  else abort(404)
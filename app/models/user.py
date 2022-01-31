from sqlalchemy.sql.functions import user
from app.db import db 
from sqlalchemy.sql import func
from sqlalchemy.sql import expression
from app.models.role import Role
from app.models.user_role import UserRole
from flask import abort

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False )
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True) 
    password = db.Column(db.String(100), nullable=False, server_default="123")
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    update_at = db.Column(db.DateTime,nullable=True, server_default=func.now())
    created_at = db.Column(db.DateTime,server_default=func.now()) 
    #Many to Many --> Rol
    roles = db.relationship(Role, secondary="user_role")
    active_role = db.Column(db.String(100), nullable=True)
   # denunciation = db.relationship('DenunciationRecord', backref='denunciation_record1', lazy=True)  

    def has_permission(cls, permission):
        for role in cls.roles:
            if (role.name == cls.active_role):
                if role.has_permission(permission):
                    return True
        return False
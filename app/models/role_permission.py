from app.db import db 
from sqlalchemy.sql import expression 
class RolePermission(db.Model):
   __tablename__ = 'role_permission'
   role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
   permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)
   active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
   #-------------
   role = db.relationship('Role', backref=db.backref("role_permission1", cascade="all, delete-orphan"))
   permission = db.relationship('Permission', backref=db.backref("role_permission2", cascade="all, delete-orphan", overlaps="permissions,role"))
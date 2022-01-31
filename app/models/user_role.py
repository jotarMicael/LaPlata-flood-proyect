from app.db import db 
from sqlalchemy.sql import expression
 
class UserRole(db.Model):
   __tablename__ = 'user_role'
   role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
   active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
   #-------------
   role = db.relationship('Role', backref=db.backref("role_permission3", cascade="all, delete-orphan"))
   user = db.relationship('User', backref=db.backref("role_permission4", cascade="all, delete-orphan"))
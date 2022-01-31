from app.db import db
from sqlalchemy.sql import expression

class Role(db.Model):
   __tablename__ = 'role'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   name = db.Column(db.String(30), nullable=False, unique=True)
   active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
  
   permissions = db.relationship("Permission", secondary="role_permission")
   users = db.relationship("User", secondary="user_role")


   def has_permission(self, permission):
      if permission in (self.permissions): 
         return True
      return False    
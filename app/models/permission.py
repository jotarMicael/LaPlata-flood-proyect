from app.db import db
from sqlalchemy.sql import expression

class Permission(db.Model):
   __tablename__ = 'permission'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   name = db.Column(db.String(30), nullable=False, unique=True)
   active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

   role = db.relationship("Role", secondary="role_permission")

       
   @classmethod
   def find_by_name(cls, permission):
      return cls.query.filter_by(name=permission).first()

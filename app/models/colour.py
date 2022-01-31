from app.db import db
from sqlalchemy.sql import expression
from flask import session 

class Colour(db.Model):
   __tablename__ = 'colour'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   name = db.Column(db.String(30), nullable=False, unique=True)
   hexa = db.Column(db.String(30), nullable=False, unique=True)
   
   system_config = db.relationship('SystemConfig', backref='colour_id1', lazy=True)


   def all():
      return Colour.query.all()

   @classmethod
   def get_hexa(cls, cid):
      colour= cls.query.get(cid)
      return colour.hexa
  
   @classmethod
   def update_session_colour(cls, id):
      colour_update = cls.get_hexa(id)
      session["hexa"] = colour_update
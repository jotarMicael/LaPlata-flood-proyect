from app.db import db
from sqlalchemy.sql import expression
from flask import session 

class ColourMap(db.Model):
   __tablename__ = 'colour_map'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
   name = db.Column(db.String(30), nullable=False, unique=True)
   hexa = db.Column(db.String(30), nullable=False, unique=True)
   
   flood_zone_colour = db.relationship('FloodZone', backref='flood_zone_colour_id', lazy=True)

   @classmethod
   def all(cls):
      return ColourMap.query.all()

   @classmethod
   def get_colour(cls,id):
      return ColourMap.query.get(id)

   @classmethod
   def get_colour_json(cls,id):
       a = db.session.query(ColourMap.hexa.label("color")).filter(
            ColourMap.id==id
        )
       return [ar._asdict() for ar in a]

   @classmethod
   def get_hexa(cls, cid):
      colour= cls.query.get(cid)
      return colour.hexa
  
   
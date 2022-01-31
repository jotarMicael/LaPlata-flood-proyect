from app.db import db
from sqlalchemy.sql import expression
from flask import abort, session

from app.models.colour import Colour

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True)
    elements_per_page = db.Column(db.Integer)
    criteria = db.Column(db.String(50))
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)  

     # One to Many --> Colour
    colour_id = db.Column(db.Integer, db.ForeignKey('colour.id'), nullable=False)
    
    @classmethod
    def get_elements_per_page(args):
        return int(SystemConfig.query.filter_by(active=1)[0].elements_per_page)

    
   
    @classmethod
    def get_config(self):
        return db.session.query(SystemConfig.id,SystemConfig.title,SystemConfig.elements_per_page,SystemConfig.criteria,SystemConfig.active, SystemConfig.colour_id, Colour.id, Colour.name).join(Colour).filter(SystemConfig.colour_id==Colour.id).all()

    
    @classmethod
    def update_config(self,parameters):
        return self.modify_config(parameters)
        
    @classmethod
    def get_config_act(self):
        return self.query.first()

   
    @classmethod
    def modify_config(self, parameters):
        config_to_update = self.get_config_act()
        
        config_to_update.title = parameters["title"]
        
        config_to_update.elements_per_page = parameters["number"]
        
        config_to_update.criteria = parameters["criteria"]
        
        config_to_update.colour_id = parameters["colour"]   
        db.session.commit()
        return {'message': 'La configuracion fue actualizada con exito!', 'category': 'success'}

    @classmethod
    def update_session_criteria(cls,criteria):
      session["criteria"] = criteria
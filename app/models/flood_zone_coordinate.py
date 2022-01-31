from app.db import db
from sqlalchemy.sql import expression
from sqlalchemy import update

class FloodZoneCoordinate(db.Model):
    __tablename__ = 'flood_zone_coordinate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    latitude = db.Column(db.String(60), server_default="0")
    longitude = db.Column(db.String(60), server_default="0")
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    
    flood_zone_id = db.Column(db.Integer, db.ForeignKey('flood_zone.id'), nullable=False)

    @classmethod
    def coordinates_deletes (cls,id):
        FloodZoneCoordinate.query.filter_by(flood_zone_id=id).update(dict(active=0) )
        db.session.commit()

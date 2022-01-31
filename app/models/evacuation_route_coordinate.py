from app.db import db
from sqlalchemy.sql import expression
from sqlalchemy import update

class EvacuationRouteCoordinate(db.Model):
    __tablename__ = 'evacuation_route_coordinate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    latitude = db.Column(db.String(60), server_default="0")
    longitude = db.Column(db.String(60), server_default="0")
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    evacuation_route_id = db.Column(db.Integer, db.ForeignKey('evacuation_route.id'), nullable=False)

    @classmethod
    def coordinates_deletes (cls,id):
        EvacuationRouteCoordinate.query.filter_by(evacuation_route_id=id).update(dict(active=0) )
        db.session.commit()

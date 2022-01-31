from app.db import db
from sqlalchemy.sql import expression
from sqlalchemy.sql import func

class EvacuationRoute(db.Model):
    __tablename__ = 'evacuation_route'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False) 
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False) 
    evacuation_route_coordinate = db.relationship('EvacuationRouteCoordinate', backref='evacuation_route_coordinate_id', lazy=True)
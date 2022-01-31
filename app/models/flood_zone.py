from app.db import db
from sqlalchemy.sql import expression

class FloodZone(db.Model):
    __tablename__ = 'flood_zone'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=True, unique=True)
    points_count = db.Column(db.Integer, server_default="0", nullable=True)
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    flood_zone_coordinate = db.relationship('FloodZoneCoordinate', backref='flood_zone_coordinate_id', lazy=True)
    colour_map_id = db.Column(db.Integer, db.ForeignKey('colour_map.id'), nullable=True)
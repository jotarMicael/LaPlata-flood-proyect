from app.db import db
from sqlalchemy.sql import expression

class MeetingSpot(db.Model):
    __tablename__ = 'meeting_spot'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)
   
    # One to Many --> State
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

   # state = db.relationship("State", foreign_keys=[state_id])
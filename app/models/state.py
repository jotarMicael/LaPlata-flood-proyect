from app.db import db

class Status(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    
    meeting_spot = db.relationship('MeetingSpot', backref='state_id1', lazy=True)
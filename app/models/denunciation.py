from app.db import db
from sqlalchemy.sql import expression
from sqlalchemy.sql import func

class Denunciation(db.Model):
    __tablename__ = 'denunciation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime,server_default=func.now()) 
    closed_at = db.Column(db.DateTime,nullable=True) 
    description = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.String(255), nullable=True)
    longitude = db.Column(db.String(255), nullable=True)
    last_name_d = db.Column(db.String(255), nullable=True)
    first_name_d = db.Column(db.String(255), nullable=True)
    phone_d = db.Column(db.String(255), nullable=True)
    email_d = db.Column(db.String(255), nullable=True)
    attempts = db.Column(db.Integer, nullable=True, server_default="0")
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    denunciation_state_id = db.Column(db.Integer, db.ForeignKey('denunciation_state.id'), nullable=False, server_default="1")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    denunciation_record = db.relationship('DenunciationRecord', backref='denunciation_id3', lazy=True)
   
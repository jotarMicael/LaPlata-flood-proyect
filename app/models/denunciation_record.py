from app.db import db
from sqlalchemy.sql import func

class DenunciationRecord(db.Model):
    __tablename__ = 'denunciation_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    created_at_r = db.Column(db.DateTime,server_default=func.now())
    user_assign = db.Column(db.String(255), nullable=True)
    actual_state = db.Column(db.String(255), nullable=True)

   # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    denunciation_id = db.Column(db.Integer, db.ForeignKey('denunciation.id'), nullable=False)
from app.db import db
from sqlalchemy.sql import expression


class DenunciationState(db.Model):
    __tablename__ = 'denunciation_state'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name_ds = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    color_class = db.Column(db.String(255), nullable=True)

    denunciation = db.relationship('Denunciation', backref='denunciation_id1', lazy=True)
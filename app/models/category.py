from app.db import db
from sqlalchemy.sql import expression
from flask import abort

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name_cat = db.Column(db.String(25), nullable=True)
    active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    denunciation = db.relationship('Denunciation', backref='denunciation_id2', lazy=True)

    @classmethod
    def get_all_categories (cls):
        return Category.query.all()

    @classmethod
    def json_categories(cls):
        a = db.session.query(Category.id,Category.name_cat).filter(
            Category.active==1
        )
        return [ar._asdict() for ar in a] if a else abort(404)

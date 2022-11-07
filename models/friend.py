from init import db
from datetime import datetime

class Friend(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    friend1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    friend1 = db.relationship('User', back_populates='friends1', foreign_keys='Friend.friend1_id')
    friend2 = db.relationship('User', back_populates='friends2', foreign_keys='Friend.friend2_id')
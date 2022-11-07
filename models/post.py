from init import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')
    post_reacts = db.relationship('PostReact', back_populates='post')
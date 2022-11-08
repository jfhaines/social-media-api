from init import db
from datetime import datetime

class PostReact(db.Model):
    __tablename__ = 'post_reacts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='post_reacts')
    post = db.relationship('Post', back_populates='post_reacts')
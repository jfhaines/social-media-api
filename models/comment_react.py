from init import db
from datetime import datetime

class CommentReact(db.Model):
    __tablename__ = 'comment_reacts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)

    user = db.relationship('User', back_populates='comment_reacts')
    comment = db.relationship('Comment', back_populates='comment_reacts')
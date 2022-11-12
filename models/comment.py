from init import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
    comment_reacts = db.relationship('CommentReact', back_populates='comment', cascade='all, delete')

    __table_args__ = (db.CheckConstraint('char_length(text) >=1 and char_length(text) <= 400', 'valid_comment_text_length_cc'),)
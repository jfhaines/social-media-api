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

    __table_args__ = (db.CheckConstraint("title ~ '[a-zA-Z0-9!?]*'", 'valid_post_title_chars_cc'),
                      db.CheckConstraint('char_length(title) >=1 and char_length(title) <=150', 'valid_post_title_length_cc'),
                      db.CheckConstraint("text ~ '[a-zA-Z0-9!?]*'", 'valid_post_text_chars_cc'),
                      db.CheckConstraint('char_length(text) >=1 and char_length(text) <= 400', 'valid_post_text_length_cc'),
                      db.CheckConstraint('date_time <= NOW()', 'valid_post_date_time_cc'))
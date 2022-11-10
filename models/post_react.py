from init import db
from datetime import datetime

class PostReact(db.Model):
    __tablename__ = 'post_reacts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('User', back_populates='post_reacts')
    post = db.relationship('Post', back_populates='post_reacts')

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='post_react_uc'),
                      db.CheckConstraint("type > 0 and type < 6", 'valid_post_react_type_cc'),
                      db.CheckConstraint('date_time <= NOW()', 'valid_post_react_date_time_cc'))
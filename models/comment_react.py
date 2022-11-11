from init import db
from datetime import datetime

class CommentReact(db.Model):
    __tablename__ = 'comment_reacts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)

    user = db.relationship('User', back_populates='comment_reacts')
    comment = db.relationship('Comment', back_populates='comment_reacts')

    __table_args__ = (db.UniqueConstraint('user_id', 'comment_id', name='comment_react_uc'),
                      db.CheckConstraint("type > 0 and type < 6", 'valid_comment_react_type_cc'))
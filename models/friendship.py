from init import db
from datetime import datetime

class Friendship(db.Model):
    __tablename__ = 'friendships'

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requester = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    user1 = db.relationship('User', back_populates='friendships1', foreign_keys='Friendship.user1_id')
    user2 = db.relationship('User', back_populates='friendships2', foreign_keys='Friendship.user2_id')

    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id', name='friendship_users_uc'),
                      db.CheckConstraint('user1_id < user2_id', name='friendship_user_ids_sorted_cc'),
                      db.CheckConstraint('requester >= 1 and requester <=2', 'valid_friendship_requester_cc'),
                      db.CheckConstraint('status >= 0 and status <=1', 'valid_friendship_status_cc'))
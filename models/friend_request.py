from init import db
from datetime import datetime
from sqlalchemy.orm import relationship

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
  
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('sender_id', 'receiver_id', name='sender_receiver_uc'),)

    sender = relationship('User', back_populates='friend_requests_sent', foreign_keys='FriendRequest.sender_id')
    receiver = relationship('User', back_populates='friend_requests_received', foreign_keys='FriendRequest.receiver_id')
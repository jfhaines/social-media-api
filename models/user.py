from init import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    post_reacts = db.relationship('PostReact', back_populates='user')
    comment_reacts = db.relationship('CommentReact', back_populates='user')
    
    friend_requests_sent = db.relationship('FriendRequest', back_populates='sender', foreign_keys='FriendRequest.sender_id')
    friend_requests_received = db.relationship('FriendRequest', back_populates='receiver', foreign_keys='FriendRequest.receiver_id')

    friends1 = db.relationship('Friend', back_populates='friend1', foreign_keys='Friend.friend1_id')
    friends2 = db.relationship('Friend', back_populates='friend2', foreign_keys='Friend.friend2_id')
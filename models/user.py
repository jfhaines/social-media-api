from init import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    post_reacts = db.relationship('PostReact', back_populates='user')
    comment_reacts = db.relationship('CommentReact', back_populates='user')

    friendships1 = db.relationship('Friendship', back_populates='user1', foreign_keys='Friendship.user1_id')
    friendships2 = db.relationship('Friendship', back_populates='user2', foreign_keys='Friendship.user2_id')

    __table_args__ = (db.CheckConstraint("username ~ '[a-zA-Z0-9!?]*'", 'valid_username_chars_cc'),
                      db.CheckConstraint('char_length(username) >= 1 and char_length(username) <=100', 'valid_username_length_cc'),
                      db.CheckConstraint("email ~ '[a-zA-Z0-9._]+@[a-zA-Z0-9._]+.com[a-zA-Z.]*'", 'valid_email_cc'),
                      db.CheckConstraint('dob < NOW()::date', 'valid_dob_cc'))
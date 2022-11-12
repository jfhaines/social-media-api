from init import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    posts = db.relationship('Post', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')
    post_reacts = db.relationship('PostReact', back_populates='user', cascade='all, delete')
    comment_reacts = db.relationship('CommentReact', back_populates='user', cascade='all, delete')

    friendships1 = db.relationship('Friendship', back_populates='user1', foreign_keys='Friendship.user1_id', cascade='all, delete')
    friendships2 = db.relationship('Friendship', back_populates='user2', foreign_keys='Friendship.user2_id', cascade='all, delete')

    __table_args__ = (db.CheckConstraint("username ~ '^[a-zA-Z0-9_.-]+$'", 'valid_username_chars_cc'),
                      db.CheckConstraint('char_length(username) >= 1 and char_length(username) <=100', 'valid_username_length_cc'),
                      db.CheckConstraint("email ~ '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'", 'valid_email_cc'),
                      db.CheckConstraint('dob < NOW()::date', 'valid_dob_cc'))
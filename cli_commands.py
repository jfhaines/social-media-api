from flask import Blueprint
from models.user import User
from models.post import Post
from models.comment import Comment
from models.post_react import PostReact
from models.comment_react import CommentReact
from models.friendship import Friendship
from init import db, bcrypt
from datetime import date, datetime
from flask_jwt_extended import jwt_required

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print('Tables dropped')

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            username='user1',
            email='user1@example.com',
            password=bcrypt.generate_password_hash('password', 10).decode('utf-8'),
            is_admin=True,
            dob=date(1998, 5, 6)
        ),
        User(
            username='user2',
            email='user2@example.com',
            password=bcrypt.generate_password_hash('password', 10).decode('utf-8'),
            is_admin=False,
            dob=date(2000, 10, 9)
        ),
        User(
            username='user3',
            email='user3@example.com',
            password=bcrypt.generate_password_hash('password', 10).decode('utf-8'),
            is_admin=False,
            dob=date(2002, 11, 5)
        ),
        User(
            username='user4',
            email='user4@example.com',
            password=bcrypt.generate_password_hash('password', 10).decode('utf-8'),
            is_admin=False,
            dob=date(2001, 4, 27)
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    posts = [
        Post(
            title='Example Post 1',
            text='This is example text.',
            date_time=datetime.now(),
            user_id=users[0].id
        ),
        Post(
            title='Example Post 2',
            text='This is also example text.',
            date_time=datetime.now(),
            user_id=users[1].id
        )
    ]
    db.session.add_all(posts)
    db.session.commit()

    comments = [
        Comment(
            text='This is a comment.',
            date_time=datetime.now(),
            user_id=users[0].id,
            post_id=posts[1].id
        ),
        Comment(
            text='This is also a comment.',
            date_time=datetime.now(),
            user_id=users[1].id,
            post_id=posts[0].id
        )
    ]
    db.session.add_all(comments)
    db.session.commit()

    post_reacts = [
        PostReact(
            type=1,
            date_time=datetime.now(),
            user_id=users[0].id,
            post_id=posts[1].id
        ),
        PostReact(
            type=2,
            date_time=datetime.now(),
            user_id=users[1].id,
            post_id=posts[0].id
        )
    ]
    db.session.add_all(post_reacts)
    db.session.commit()

    comment_reacts = [
        CommentReact(
            type=4,
            date_time=datetime.now(),
            user_id=users[0].id,
            comment_id=comments[1].id
        ),
        CommentReact(
            type=5,
            date_time=datetime.now(),
            user_id=users[1].id,
            comment_id=comments[0].id
        )
    ]
    db.session.add_all(comment_reacts)
    db.session.commit()

    friendships = [
        Friendship(
            user1_id=users[0].id,
            user2_id=users[1].id,
            date_time=datetime.now(),
            requester=1,
            status=0
        ),
        Friendship(
            user1_id=users[2].id,
            user2_id=users[3].id,
            date_time=datetime.now(),
            requester=2,
            status=1
        )
    ]
    db.session.add_all(friendships)
    db.session.commit()

    print('Tables seeded')

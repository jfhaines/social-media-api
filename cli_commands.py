from flask import Blueprint
from models.user import User
from models.post import Post
from models.comment import Comment
from models.post_react import PostReact
from models.comment_react import CommentReact
from models.friend import Friend
from models.friend_request import FriendRequest
from init import db, bcrypt
from datetime import date
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
from flask import Blueprint, request, abort
from models.user import User
from schemas.user_schema import UserSchema
from init import db, bcrypt
from datetime import date, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from utils import add_resource_to_db


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    user_data = UserSchema().load(request.json)

    user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=bcrypt.generate_password_hash(user_data['password']).decode('utf-8'),
        dob=generate_date(user_data['dob']),
        is_admin=user_data['is_admin']
    )
    # Creates and executes a query in the database which creates a new row in the user table which maps to the user instance defined above.
    # If any of the constraints below are violated during this process, an appropriate error message will be sent in response.
    add_resource_to_db(user, constraint_errors_config=[
        ('users_email_key', 409, 'You need to enter a unique email.'),
        ('users_username_key', 409, 'You need to enter a unique username.'),
        ('valid_dob_cc', 400, 'You cannot enter a date of birth that is in the future.')
    ])

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=3))
    return {'user': UserSchema(exclude=['password']).dump(user), 'jwt': token}


@auth_bp.route('/login', methods=['POST'])
def login():
    # Creates and executes a query which attempts to retrieve a user instance from the user table which has a username value that matches the username
    # provided in the request's body
    stmt = select(User).where(User.username == request.json['username'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=3))
        return {'user': UserSchema(exclude=['password']).dump(user), 'jwt': token}
    else:
        return {'error': 'Wrong email or password'}, 401



def generate_date(date_string):
    date_data = date_string.split('/')
    day = int(date_data[0])
    month = int(date_data[1])
    year = int(date_data[2])
    return date(year, month, day)
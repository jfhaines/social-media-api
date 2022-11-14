from flask import Blueprint, request, abort
from models.user import User
from schemas.user_schema import UserSchema
from init import db, bcrypt
from datetime import date, timedelta
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from controllers.auth_controller import generate_date
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation, check_authentication


users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
@jwt_required()
def read_users():
    check_authentication()
    # Sends a query to the db asking it to retrieve all user instances.
    stmt = select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def read_user(user_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    return UserSchema(exclude=['password']).dump(user)


@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    check_authentication()
    user_data = UserSchema().load(request.json, partial=True)
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    confirm_authorisation(user, action='update', resource_type='user')
    user.username = user_data.get('username') or user.username
    user.email = user_data.get('email') or user.email
    user.password = bcrypt.generate_password_hash(user_data.get('password')).decode('utf-8') if user_data.get('password') else user.password
    user.is_admin = user_data.get('is_admin') if user_data.get('is_admin') != None else user.is_admin
    user.dob = generate_date(user_data.get('dob')) if user_data.get('dob') else user.dob
    # Sends a query to the db asking it to update the row in the users table that maps to the user instance above and apply the same changes to it that were made to the model instance.
    # If one of the constraints listed below are violated during this process, then an error message and an appropriate status code will be returned.
    add_resource_to_db(constraint_errors_config=[
        ('users_email_key', 409, 'You need to enter a unique email.'),
        ('users_username_key', 409, 'You need to enter a unique username.'),
        ('valid_dob_cc', 400, 'You cannot enter a date of birth that is in the future.')
    ])
    return UserSchema().dump(user)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    confirm_authorisation(user, action='delete', resource_type='user')
    # Sends a query to the db asking it to delete the row in the users table that maps to the provided user instance.
    db.session.delete(user)
    db.session.commit()
    return {'message': f'User {user.id} deleted successfully'}
from flask import Blueprint, request, abort
from models.user import User
from schemas.user_schema import UserSchema
from init import db, bcrypt
from datetime import date, timedelta
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from controllers.auth_controller import generate_date
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation


users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
@jwt_required()
def read_users():
    stmt = select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password', 'dob', 'is_admin']).dump(users)


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def read_user(user_id):
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    return UserSchema(exclude=['password', 'dob', 'is_admin']).dump(user)


@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    user_data = UserSchema().load(request.json)
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    confirm_authorisation(user, action='update', resource_type='user')
    user.username = user_data.get('username') or user.username
    user.email = user_data.get('email') or user.email
    user.password = bcrypt.generate_password_hash(user_data.get('password')) if user_data.get('password') else user.password
    user.is_admin = user_data.get('is_admin') if user_data.get('is_admin') != None else user.is_admin
    user.dob = generate_date(user_data.get('dob')) if user_data.get('dob') else user.dob
    add_resource_to_db(constraint_errors_config=[
        ('users_email_key', 409, 'You need to enter a unique email.'),
        ('users_username_key', 409, 'You need to enter a unique username.'),
        ('valid_dob_cc', 400, 'You cannot enter a date of birth that is in the future.')
    ])
    return UserSchema().dump(user)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    confirm_authorisation(user, action='delete', resource_type='user')
    db.session.delete(user)
    db.session.commit()
    return {'message': f'User {user.id} deleted successfully'}
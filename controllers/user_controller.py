from flask import Blueprint, request, abort
from models.user import User
from schemas.user_schema import UserSchema
from init import db, bcrypt
from datetime import date, timedelta
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from controllers.auth_controller import generate_date


users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    user_data = UserSchema().load(request.json)

    stmt = select(User).where(User.id == user_id)
    user = db.session.scalar(stmt)

    jwt_id = int(get_jwt_identity())

    if user:
        if jwt_id != user_id:
            return {'error': "You are not permitted to update this user's profile"}, 401
        user.username = request.json.get('username') or user.username
        user.email = request.json.get('email') or user.email
        user.password = bcrypt.generate_password_hash(request.json.get('password')) if request.json.get('password') else user.password
        user.is_admin = request.json.get('is_admin') if request.json.get('is_admin') != None else user.is_admin
        user.dob = generate_date(request.json.get('dob')) if request.json.get('dob') else user.dob
        db.session.commit()
        return UserSchema().dump(user)
    else:
        return {'error': f'There is no user with id {user_id}'}, 404


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    stmt = select(User).where(User.id == user_id)
    user = db.session.scalar(stmt)

    jwt_id = int(get_jwt_identity())
    stmt = select(User).where(User.id == jwt_id)
    jwt_user = db.session.scalar(stmt)

    if user:
        if jwt_id != user_id and not jwt_user.is_admin:
            return {'error': "You are not permitted to delete this user's profile"}, 401
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user.id} deleted successfully'}
    else:
        return {'error': f'There is no user with id {user_id}'}, 404
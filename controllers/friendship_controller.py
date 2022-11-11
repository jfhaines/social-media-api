from flask import Blueprint, request, abort
from models.user import User
from models.friendship import Friendship
from schemas.friendship_schema import FriendshipSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select, or_
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation


friendships_bp = Blueprint('friendships', __name__, url_prefix='/users/<int:user_id>/friendships')


@friendships_bp.route('/', methods=['GET'])
@jwt_required()
def read_friendships(user_id):
    retrieve_resource_by_id(user_id, model=User, resource_type='user')
    stmt = select(Friendship).where(or_(Friendship.user1_id == user_id, Friendship.user2_id == user_id))
    friendships = db.session.scalars(stmt)
    return FriendshipSchema(many=True).dump(friendships)


@friendships_bp.route('/<int:friendship_id>', methods=['GET'])
@jwt_required()
def read_friendship(user_id, friendship_id):
    retrieve_resource_by_id(user_id, model=User, resource_type='user')
    friendship = retrieve_resource_by_id(friendship_id, model=Friendship, resource_type='friendship')
    return FriendshipSchema().dump(friendship)


@friendships_bp.route('/', methods=['POST'])
@jwt_required()
def create_friendship(user_id):
    retrieve_resource_by_id(user_id, model=User, resource_type='user')
    
    jwt_id = int(get_jwt_identity())
    if jwt_id < user_id:
        smaller_user_id = jwt_id
        larger_user_id = user_id
    else:
        smaller_user_id = user_id
        larger_user_id = jwt_id

    friendship = Friendship(
        user1_id=smaller_user_id,
        user2_id=larger_user_id,
        requester=1 if jwt_id == smaller_user_id else 2,
        date_time=datetime.now()
    )

    add_resource_to_db(friendship, constraint_errors_config=[
        ('friendship_users_uc', 409, 'The two users in this friendship must be distinct.'),
        ('friendship_user_ids_sorted_cc', 500, 'user1_id needs to be less than user2_id.')
    ])
    return FriendshipSchema().dump(friendship), 201



@friendships_bp.route('/<int:friendship_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_friendship(user_id, friendship_id):
    retrieve_resource_by_id(user_id, model=User, resource_type='user')
    friendship_data = FriendshipSchema().load(request.json)
    friendship = retrieve_resource_by_id(friendship_id, model=Friendship, resource_type='friendship')
    confirm_authorisation(friendship, action='update', resource_type='friendship')
    friendship.status = friendship_data.get('status') or friendship.status
    add_resource_to_db(constraint_errors_config=[
        ('friendship_users_uc', 409, 'The two users in this friendship must be distinct.'),
        ('friendship_user_ids_sorted_cc', 500, 'user1_id needs to be less than user2_id.')
    ])
    return FriendshipSchema().dump(friendship)


@friendships_bp.route('/<int:friendship_id>', methods=['DELETE'])
@jwt_required()
def delete_friendship(user_id, friendship_id):
    retrieve_resource_by_id(user_id, model=User, resource_type='user')
    friendship = retrieve_resource_by_id(friendship_id, model=Friendship, resource_type='friendship')
    confirm_authorisation(friendship, action='delete', resource_type='friendship')
    db.session.delete(friendship)
    db.session.commit()
    return {'message': f'Friendship  {friendship.id} deleted successfully'}
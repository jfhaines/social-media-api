from flask import Blueprint, request, abort
from models.user import User
from models.friend import Friend
from schemas.friend_schema import FriendSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


friends_bp = Blueprint('friends', __name__, url_prefix='users/<int:user_id>/friends')

@friends_bp.route('/', methods=['GET'])
@jwt_required()
def read_friends(user_id):
    stmt = select(Friend)
    friends = db.session.scalars(stmt)
    return FriendSchema(many=True).dump(friends)


@friends_bp.route('/<int:friend_id>', methods=['GET'])
@jwt_required()
def read_friend(user_id, friend_id):
    stmt = select(Friend).where(Friend.id == friend_id)
    friend = db.session.scalar(stmt)

    if friend:
        return FriendSchema().dump(friend)
    else:
        return {'error': f'There is no friend with id {friend_id}'}, 404


@friends_bp.route('/', methods=['POST'])
@jwt_required()
def create_friend(user_id):
    friend_data = FriendSchema().load(request.json)

    if friend_data.get('friend1_id') > friend_data.get('friend2_id'):
        larger_user_id = friend_data.get('friend1_id')
        smaller_user_id = friend_data.get('friend2_id')
    else:
        larger_user_id = friend_data.get('friend2_id')
        smaller_user_id = friend_data.get('friend1_id')

    friend = FriendSchema(
        friend1_id=larger_user_id,
        friend2_id=smaller_user_id,
        date_time=datetime.now()
    )

    db.session.add(friend)
    db.session.commit()
    return FriendSchema().dump(friend), 201


@friends_bp.route('/<int:friend_id>', methods=['DELETE'])
@jwt_required()
def delete_friend(user_id, friend_id):
    stmt = select(Friend).where(Friend.id == friend_id)
    friend = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if friend:
        if get_jwt_identity() == friend.friend1_id or get_jwt_identity() == friend.friend2_id or jwt_user.is_admin == True:
            db.session.delete(friend)
            db.session.commit()
            return {'message': f'Friend  {friend.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this friend"}, 401
    else:
        return {'error': f'There is no friend with id {friend_id}'}, 404
from flask import Blueprint, request, abort
from models.user import User
from models.friend_request import FriendRequest
from schemas.friend_request_schema import FriendRequestSchema
from schemas.post_schema import PostSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


friend_requests_bp = Blueprint('friend_requests', __name__, url_prefix='users/<int:user_id>/friend_requests')

@friend_requests_bp.route('/', methods=['GET'])
@jwt_required()
def read_friend_requests(user_id):
    stmt = select(FriendRequest).where(FriendRequest.receiver_id == user_id)
    friend_requests = db.session.scalars(stmt)
    return FriendRequestSchema(many=True).dump(friend_requests)


@friend_requests_bp.route('/<int:friend_request_id>', methods=['GET'])
@jwt_required()
def read_friend_request(user_id, friend_request_id):
    stmt = select(FriendRequest).where(FriendRequest.id == friend_request_id)
    friend_request = db.session.scalar(stmt)

    if friend_request:
        return FriendRequestSchema().dump(friend_request)
    else:
        return {'error': f'There is no friend request with id {friend_request_id}'}, 404


@friend_requests_bp.route('/', methods=['POST'])
@jwt_required()
def create_friend_request(user_id):
    friend_request_data = FriendRequestSchema().load(request.json)

    friend_request = FriendRequestSchema(
        sender_id=get_jwt_identity,
        receiver_id=friend_request_data.get('receiver_id'),
        date_time=datetime.now()
    )

    db.session.add(friend_request)
    db.session.commit()
    return FriendRequestSchema().dump(friend_request), 201


@friend_requests_bp.route('/<int:friend_request_id>', methods=['DELETE'])
@jwt_required()
def delete_friend_request(user_id, friend_request_id):
    stmt = select(FriendRequest).where(FriendRequest.id == friend_request_id)
    friend_request = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if friend_request:
        if get_jwt_identity() == friend_request.sender_id or jwt_user.is_admin == True:
            db.session.delete(friend_request)
            db.session.commit()
            return {'message': f'Friend request {friend_request.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this friend request"}, 401
    else:
        return {'error': f'There is no friend request with id {friend_request_id}'}, 404
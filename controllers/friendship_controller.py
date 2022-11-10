from flask import Blueprint, request, abort
from models.user import User
from models.friendship import Friendship
from schemas.friendship_schema import FriendshipSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select, or_
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


friendships_bp = Blueprint('friendships', __name__, url_prefix='/users/<int:user_id>/friendships')

@friendships_bp.route('/', methods=['GET'])
@jwt_required()
def read_friendships(user_id):
    stmt = select(Friendship).where(or_(Friendship.user1_id == user_id, Friendship.user2_id == user_id))
    friendships = db.session.scalars(stmt)
    return FriendshipSchema(many=True).dump(friendships)


@friendships_bp.route('/<int:friendship_id>', methods=['GET'])
@jwt_required()
def read_friendship(user_id, friendship_id):
    stmt = select(Friendship).where(Friendship.id == friendship_id)
    friendship = db.session.scalar(stmt)

    if friendship:
        return FriendshipSchema().dump(friendship)
    else:
        return {'error': f'There is no friendship with id {friendship_id}'}, 404


@friendships_bp.route('/', methods=['POST'])
@jwt_required()
def create_friendship(user_id):
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

    db.session.add(friendship)
    db.session.commit()
    return FriendshipSchema().dump(friendship), 201


@friendships_bp.route('/<int:friendship_id>', methods=['DELETE'])
@jwt_required()
def delete_friend(user_id, friendship_id):
    stmt = select(Friendship).where(Friendship.id == friendship_id)
    friendship = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if friendship:
        if get_jwt_identity() == friendship.user1_id or get_jwt_identity() == friendship.user2_id or jwt_user.is_admin == True:
            db.session.delete(friendship)
            db.session.commit()
            return {'message': f'Friendship  {friendship.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this friendship"}, 401
    else:
        return {'error': f'There is no friendship with id {friendship_id}'}, 404
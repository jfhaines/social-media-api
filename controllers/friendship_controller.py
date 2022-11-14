from flask import Blueprint, request, abort
from models.user import User
from models.friendship import Friendship
from schemas.friendship_schema import FriendshipSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select, or_
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation, check_authentication, is_child


friendships_bp = Blueprint('friendships', __name__, url_prefix='/users/<int:user_id>/friendships')


@friendships_bp.route('/', methods=['GET'])
@jwt_required()
def read_friendships(user_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    retrieve_resource_by_id(user_id, model=User, resource_type='user')
    # Sends a query to the db asking it to retrieve all friendship instances that have a user1_id or user2_id that matches the user_id provided as a parameter in the route.
    stmt = select(Friendship).where(or_(Friendship.user1_id == user_id, Friendship.user2_id == user_id))
    friendships = db.session.scalars(stmt)
    return FriendshipSchema(many=True).dump(friendships)


@friendships_bp.route('/<int:friendship_id>', methods=['GET'])
@jwt_required()
def read_friendship(user_id, friendship_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    # Sends a query to the db asking it to retrieve a friendship instance that has an id that matches the friendship_id provided as a parameter in the route.
    # If no friendship has that id, a customised error message will be sent with an appropriate status code.
    friendship = retrieve_resource_by_id(friendship_id, model=Friendship, resource_type='friendship')
    is_child(parent=user, child=friendship, id_str=['user1_id', 'user2_id'])
    return FriendshipSchema().dump(friendship)


@friendships_bp.route('/', methods=['POST'])
@jwt_required()
def create_friendship(user_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
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
    # Sends a query to the db asking it to create a new row in the friendships table which maps to the friendship instance defined above.
    # During this process, if the constraints listed below are violated, an appropriate error message and status code will be sent in response.
    add_resource_to_db(friendship, constraint_errors_config=[
        ('friendship_users_uc', 409, 'These two users already have an existing friendship.'),
        ('friendship_user_ids_sorted_cc', 400, 'user1_id must be smaller than user2_id.')
    ])
    return FriendshipSchema().dump(friendship), 201



@friendships_bp.route('/<int:friendship_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_friendship(user_id, friendship_id):
    check_authentication()
    friendship_data = FriendshipSchema().load(request.json, partial=True)
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    # Sends a query to the db asking it to retrieve a friendship instance that has an id that matches the friendship_id provided as a parameter in the route.
    # If no friendship has that id, a customised error message will be sent with an appropriate status code.
    friendship = retrieve_resource_by_id(friendship_id, model=Friendship, resource_type='friendship')
    is_child(parent=user, child=friendship, id_str=['user1_id', 'user2_id'])
    confirm_authorisation(friendship, action='update', resource_type='friendship')
    friendship.status = friendship_data.get('status') if friendship_data.get('status') != None else friendship.status
    # Sends a query to the db asking it to update the row in the friendships table that maps to the friendship instance above and apply the same changes to it that were made to the model instance.
    db.session.commit()
    return FriendshipSchema().dump(friendship)


@friendships_bp.route('/<int:friendship_id>', methods=['DELETE'])
@jwt_required()
def delete_friendship(user_id, friendship_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a user instance that has an id that matches the user_id provided as a parameter in the route.
    # If no user has that id, a customised error message will be sent with an appropriate status code.
    user = retrieve_resource_by_id(user_id, model=User, resource_type='user')
    # Sends a query to the db asking it to retrieve a friendship instance that has an id that matches the friendship_id provided as a parameter in the route.
    # If no friendship has that id, a customised error message will be sent with an appropriate status code.
    friendship = retrieve_resource_by_id(friendship_id, model=Friendship, resource_type='friendship')
    is_child(parent=user, child=friendship, id_str=['user1_id', 'user2_id'])
    confirm_authorisation(friendship, action='delete', resource_type='friendship')
    # Sends a query to the db asking it to delete the row in the friendships table that maps to the provided friendship instance.
    db.session.delete(friendship)
    db.session.commit()
    return {'message': f'Friendship  {friendship.id} deleted successfully'}
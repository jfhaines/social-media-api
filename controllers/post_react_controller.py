from flask import Blueprint, request, abort
from models.user import User
from models.post import Post
from models.post_react import PostReact
from schemas.post_react_schema import PostReactSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation, check_authentication, is_child


post_reacts_bp = Blueprint('post_reacts', __name__, url_prefix='/posts/<int:post_id>/reacts')

@post_reacts_bp.route('/', methods=['GET'])
@jwt_required()
def read_post_reacts(post_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve all post react instances that have a post_id that matches the post_id provided in the route.
    stmt = select(PostReact).where(PostReact.post_id == post_id)
    post_reacts = db.session.scalars(stmt)
    return PostReactSchema(many=True).dump(post_reacts)


@post_reacts_bp.route('/<int:post_react_id>', methods=['GET'])
@jwt_required()
def read_post_react(post_id, post_react_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a post react instance that has an id that matches the post_react_id provided as a parameter in the route.
    # If no post react has that id, a customised error message will be sent with an appropriate status code.
    post_react = retrieve_resource_by_id(post_react_id, model=PostReact, resource_type='post react')
    is_child(parent=post, child=post_react, id_str='post_id')
    return PostReactSchema().dump(post_react)


@post_reacts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post_react(post_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    post_react_data = PostReactSchema(exclude=['user_id', 'post_id']).load(request.json)
    post_react = PostReact(
        type=post_react_data.get('type'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        post_id=post_id
    )
    # Sends a query to the db asking it to create a new row in the post_reacts table which maps to the post_react instance defined above.
    # During this process, if the constraint listed below is violated, an appropriate error message and status code will be sent in response.
    add_resource_to_db(post_react, constraint_errors_config=[('post_react_uc', 409, 'A user can only react once to a post.')])
    return PostReactSchema().dump(post_react), 201


@post_reacts_bp.route('/<int:post_react_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post_react(post_id, post_react_id):
    check_authentication()
    post_react_data = PostReactSchema().load(request.json, partial=True)
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a post react instance that has an id that matches the post_react_id provided as a parameter in the route.
    # If no post react has that id, a customised error message will be sent with an appropriate status code.
    post_react = retrieve_resource_by_id(post_react_id, model=PostReact, resource_type='post react')
    is_child(parent=post, child=post_react, id_str='post_id')
    confirm_authorisation(post_react, action='update', resource_type='post react')
    post_react.type = post_react_data.get('type') or post_react.type
    # Sends a query to the db asking it to update the row in the post_reacts table that maps to the post_react instance above and apply the same changes to it that were made to the model instance.
    db.session.commit()
    return PostReactSchema().dump(post_react)


@post_reacts_bp.route('/<int:post_react_id>', methods=['DELETE'])
@jwt_required()
def delete_post_react(post_id, post_react_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a post react instance that has an id that matches the post_react_id provided as a parameter in the route.
    # If no post react has that id, a customised error message will be sent with an appropriate status code.
    post_react = retrieve_resource_by_id(post_react_id, model=PostReact, resource_type='post react')
    is_child(parent=post, child=post_react, id_str='post_id')
    confirm_authorisation(post_react, action='delete', resource_type='post react')
    # Sends a query to the db asking it to delete the row in the post_reacts table that maps to the provided post_react instance.
    db.session.delete(post_react)
    db.session.commit()
    return {'message': f'Post react {post_react.id} deleted successfully'}

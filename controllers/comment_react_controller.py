from flask import Blueprint, request, abort
from models.user import User
from models.post import Post
from models.comment import Comment
from models.comment_react import CommentReact
from schemas.comment_react_schema import CommentReactSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation, check_authentication, is_child


comment_reacts_bp = Blueprint('comment_reacts', __name__, url_prefix='/posts/<int:post_id>/comments/<int:comment_id>/reacts')


@comment_reacts_bp.route('/', methods=['GET'])
@jwt_required()
def read_comment_reacts(post_id, comment_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    # Sends a query to the db asking it to retrieve all comment react instances that have a comment_id that matches the comment_id provided in the route.
    stmt = select(CommentReact).where(CommentReact.comment_id == comment_id)
    comment_reacts = db.session.scalars(stmt)
    return CommentReactSchema(many=True).dump(comment_reacts)


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['GET'])
@jwt_required()
def read_comment_react(post_id, comment_id, comment_react_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    # Sends a query to the db asking it to retrieve a comment react instance that has an id that matches the comment_react_id provided as a parameter in the route.
    # If no comment react has that id, a customised error message will be sent with an appropriate status code.
    comment_react = retrieve_resource_by_id(comment_react_id, model=CommentReact, resource_type='comment react')
    is_child(parent=post, child=comment, id_str='post_id')
    is_child(parent=comment, child=comment_react, id_str='comment_id')
    return CommentReactSchema().dump(comment_react)



@comment_reacts_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment_react(post_id, comment_id):
    check_authentication()
    comment_react_data = CommentReactSchema(exclude=['user_id', 'comment_id']).load(request.json)
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    comment_react = CommentReact(
        type=comment_react_data.get('type'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        comment_id=comment_id
    )
    # Sends a query to the db asking it to create a new row in the comment_reacts table which maps to the comment_react instance defined above.
    # During this process, if the constraint listed below is violated, an appropriate error message and status code will be sent in response.
    add_resource_to_db(comment_react, constraint_errors_config=[('comment_react_uc', 409, 'A user can only react once to a comment.')])
    return CommentReactSchema().dump(comment_react), 201


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment_react(post_id, comment_id, comment_react_id):
    check_authentication()
    comment_react_data = CommentReactSchema().load(request.json, partial=True)
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    # Sends a query to the db asking it to retrieve a comment react instance that has an id that matches the comment_react_id provided as a parameter in the route.
    # If no comment react has that id, a customised error message will be sent with an appropriate status code.
    comment_react = retrieve_resource_by_id(comment_react_id, model=CommentReact, resource_type='comment react')
    is_child(parent=post, child=comment, id_str='post_id')
    is_child(parent=comment, child=comment_react, id_str='comment_id')
    confirm_authorisation(comment_react, action='update', resource_type='comment react')
    comment_react.type = comment_react_data.get('type') or comment_react.type
    # Sends a query to the db asking it to update the row in the comment_reacts table that maps to the comment_react instance above and apply the same changes to it that were made to the model instance.
    db.session.commit()
    return CommentReactSchema().dump(comment_react)


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['DELETE'])
@jwt_required()
def delete_comment_react(post_id, comment_id, comment_react_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    # Sends a query to the db asking it to retrieve a comment react instance that has an id that matches the comment_react_id provided as a parameter in the route.
    # If no comment react has that id, a customised error message will be sent with an appropriate status code.
    comment_react = retrieve_resource_by_id(comment_react_id, model=CommentReact, resource_type='comment react')
    is_child(parent=post, child=comment, id_str='post_id')
    is_child(parent=comment, child=comment_react, id_str='comment_id')
    confirm_authorisation(comment_react, action='delete', resource_type='comment react')
    # Sends a query to the db asking it to delete the row in the comment_reacts table that maps to the provided comment_react instance.
    db.session.delete(comment_react)
    db.session.commit()
    return {'message': f'Comment react {comment_react.id} deleted successfully'}
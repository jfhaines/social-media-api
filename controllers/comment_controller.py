from flask import Blueprint, request, abort, Response
from models.user import User
from models.comment import Comment
from models.post import Post
from schemas.comment_schema import CommentSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from custom_errors import HttpError
from utils import confirm_authorisation, retrieve_resource_by_id, add_resource_to_db, check_authentication, is_child


comments_bp = Blueprint('comments', __name__, url_prefix='/posts/<int:post_id>/comments')


@comments_bp.route('/', methods=['GET'])
@jwt_required()
def read_comments(post_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking to retrieve all comment instances that have a post_id that matches the post_id provided in the route.
    stmt = select(Comment).where(Comment.post_id == post_id)
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)


@comments_bp.route('/<int:comment_id>', methods=['GET'])
@jwt_required()
def read_comment(post_id, comment_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    return CommentSchema().dump(comment)


@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment_data = CommentSchema(exclude=['user_id', 'post_id']).load(request.json)
    comment = Comment(
        text=comment_data.get('text'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        post_id=post_id
    )
    # Sends a query to the db asking it to create a new row in the comments table which maps to the comment instance defined above.
    db.session.add(comment)
    db.session.commit()
    return CommentSchema().dump(comment), 201


@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(post_id, comment_id):
    check_authentication()
    comment_data = CommentSchema().load(request.json, partial=True)
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    confirm_authorisation(comment, action='update', resource_type='comment')
    comment.text = comment_data.get('text') or comment.text
    # Sends a query to the db asking it to update the row in the comments table that maps to the comment instance above and apply the same changes to it that were made to the model instance.
    db.session.commit()
    return CommentSchema().dump(comment)


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(post_id, comment_id):
    check_authentication()
    # Sends a query to the db asking it to retrieve a post instance that has an id that matches the post_id provided as a parameter in the route.
    # If no post has that id, a customised error message will be sent with an appropriate status code.
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    # Sends a query to the db asking it to retrieve a comment instance that has an id that matches the comment_id provided as a parameter in the route.
    # If no comment has that id, a customised error message will be sent with an appropriate status code.
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    confirm_authorisation(comment, action='delete', resource_type='comment')
    # Sends a query to the db asking it to delete the row in the comments table that maps to the provided comment instance.
    db.session.delete(comment)
    db.session.commit()
    return {'message': f'Comment {comment.id} deleted successfully'}
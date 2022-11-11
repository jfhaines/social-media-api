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
from utils import confirm_authorisation, retrieve_resource_by_id, add_resource_to_db


comments_bp = Blueprint('comments', __name__, url_prefix='/posts/<int:post_id>/comments')


@comments_bp.route('/', methods=['GET'])
@jwt_required()
def read_comments(post_id):
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    stmt = select(Comment).where(Comment.post_id == post_id)
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)


@comments_bp.route('/<int:comment_id>', methods=['GET'])
@jwt_required()
def read_comment(post_id, comment_id):
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    return CommentSchema().dump(comment)


@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment_data = CommentSchema().load(request.json)
    comment = Comment(
        text=comment_data.get('text'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        post_id=post_id
    )
    db.session.add(comment)
    db.session.commit()
    return CommentSchema().dump(comment), 201


@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(post_id, comment_id):
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment_data = CommentSchema().load(request.json)
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    confirm_authorisation(comment, action='update', resouce_type='comment')
    comment.text = comment_data.get('text') or comment.text
    db.session.commit()
    return CommentSchema().dump(comment)


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(post_id, comment_id):
    retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    confirm_authorisation(comment, action='delete', resouce_type='comment')
    db.session.delete(comment)
    db.session.commit()
    return {'message': f'Comment {comment.id} deleted successfully'}
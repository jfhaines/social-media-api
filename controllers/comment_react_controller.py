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
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    stmt = select(CommentReact).where(CommentReact.comment_id == comment_id)
    comment_reacts = db.session.scalars(stmt)
    return CommentReactSchema(many=True).dump(comment_reacts)


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['GET'])
@jwt_required()
def read_comment_react(post_id, comment_id, comment_react_id):
    check_authentication()
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    comment_react = retrieve_resource_by_id(comment_react_id, model=CommentReact, resource_type='comment react')
    is_child(parent=post, child=comment, id_str='post_id')
    is_child(parent=comment, child=comment_react, id_str='comment_id')
    return CommentReactSchema().dump(comment_react)



@comment_reacts_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment_react(post_id, comment_id):
    check_authentication()
    comment_react_data = CommentReactSchema(exclude=['user_id', 'comment_id']).load(request.json)
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    is_child(parent=post, child=comment, id_str='post_id')
    comment_react = CommentReact(
        type=comment_react_data.get('type'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        comment_id=comment_id
    )
    add_resource_to_db(comment_react, constraint_errors_config=[('comment_react_uc', 409, 'A user can only react once to a comment.')])
    return CommentReactSchema().dump(comment_react), 201


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment_react(post_id, comment_id, comment_react_id):
    check_authentication()
    comment_react_data = CommentReactSchema().load(request.json, partial=True)
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    comment_react = retrieve_resource_by_id(comment_react_id, model=CommentReact, resource_type='comment react')
    is_child(parent=post, child=comment, id_str='post_id')
    is_child(parent=comment, child=comment_react, id_str='comment_id')
    confirm_authorisation(comment_react, action='update', resource_type='comment react')
    comment_react.type = comment_react_data.get('type') or comment_react.type
    db.session.commit()
    return CommentReactSchema().dump(comment_react)


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['DELETE'])
@jwt_required()
def delete_comment_react(post_id, comment_id, comment_react_id):
    check_authentication()
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    comment = retrieve_resource_by_id(comment_id, model=Comment, resource_type='comment')
    comment_react = retrieve_resource_by_id(comment_react_id, model=CommentReact, resource_type='comment react')
    is_child(parent=post, child=comment, id_str='post_id')
    is_child(parent=comment, child=comment_react, id_str='comment_id')
    confirm_authorisation(comment_react, action='delete', resource_type='comment react')
    db.session.delete(comment_react)
    db.session.commit()
    return {'message': f'Comment react {comment_react.id} deleted successfully'}
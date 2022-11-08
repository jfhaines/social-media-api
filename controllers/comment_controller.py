from flask import Blueprint, request, abort
from models.user import User
from models.comment import Comment
from schemas.comment_schema import CommentSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


comments_bp = Blueprint('comments', __name__, url_prefix='/posts/<int:post_id>/comments')

@comments_bp.route('/', methods=['GET'])
@jwt_required()
def read_comments(post_id):
    stmt = select(Comment).where(Comment.post_id == post_id)
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)


@comments_bp.route('/<int:comment_id>', methods=['GET'])
@jwt_required()
def read_comment(post_id, comment_id):
    stmt = select(Comment).where(Comment.id == comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        return CommentSchema().dump(comment)
    else:
        return {'error': f'There is no comment with id {comment_id}'}, 404


@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(post_id):
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
    comment_data = CommentSchema().load(request.json)

    stmt = select(Comment).where(Comment.id == comment_id)
    comment = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if comment:
        if get_jwt_identity() == comment.user_id or jwt_user.is_admin == True:
            comment.text = comment_data.get('text') or comment.text
            db.session.commit()
            return CommentSchema().dump(comment)
        else:
            return {'error': "You are not permitted to update this comment"}, 401
    else:
        return {'error': f'There is no comment with id {comment_id}'}, 404


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(post_id, comment_id):
    stmt = select(Comment).where(Comment.id == comment_id)
    comment = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if comment:
        if get_jwt_identity() == comment.user_id or jwt_user.is_admin == True:
            db.session.delete(comment)
            db.session.commit()
            return {'message': f'Comment {comment.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this comment"}, 401
    else:
        return {'error': f'There is no comment with id {comment_id}'}, 404
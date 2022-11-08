from flask import Blueprint, request, abort
from models.user import User
from models.comment_react import CommentReact
from schemas.comment_react_schema import CommentReactSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


comment_reacts_bp = Blueprint('comment_reacts', __name__, url_prefix='posts/<int:post_id>/comments/<int:comment_id>/comment_reacts')

@comment_reacts_bp.route('/', methods=['GET'])
@jwt_required()
def read_comment_reacts(post_id, comment_id):
    stmt = select(CommentReact).where(CommentReact.comment_id == comment_id)
    comment_reacts = db.session.scalars(stmt)
    return CommentReactSchema(many=True).dump(comment_reacts)


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['GET'])
@jwt_required()
def read_comment_react(post_id, comment_id, comment_react_id):
    stmt = select(CommentReact).where(CommentReact.id == comment_react_id)
    comment_react = db.session.scalar(stmt)

    if comment_react:
        return CommentReactSchema().dump(comment_react)
    else:
        return {'error': f'There is no comment react with id {comment_react_id}'}, 404


@comment_reacts_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment_react(post_id, comment_id):
    comment_react_data = CommentReactSchema().load(request.json)

    comment_react = CommentReactSchema(
        type=comment_react_data.get('type'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        comment_id=comment_id
    )

    db.session.add(comment_react)
    db.session.commit()
    return CommentReactSchema().dump(comment_react), 201


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment_react(post_id, comment_id, comment_react_id):
    comment_react_data = CommentReactSchema().load(request.json)

    stmt = select(CommentReact).where(CommentReact.id == comment_react_id)
    comment_react = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if comment_react:
        if get_jwt_identity() == comment_react.user_id or jwt_user.is_admin == True:
            comment_react.type = comment_react_data.get('type') or comment_react.type
            db.session.commit()
            return CommentReactSchema().dump(comment_react)
        else:
            return {'error': "You are not permitted to update this comment react"}, 401
    else:
        return {'error': f'There is no comment react with id {comment_react_id}'}, 404


@comment_reacts_bp.route('/<int:comment_react_id>', methods=['DELETE'])
@jwt_required()
def delete_comment_react(post_id, comment_id, comment_react_id):
    stmt = select(CommentReact).where(CommentReact.id == comment_react_id)
    comment_react = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if comment_react:
        if get_jwt_identity() == comment_react.user_id or jwt_user.is_admin == True:
            db.session.delete(comment_react)
            db.session.commit()
            return {'message': f'Comment react {comment_react.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this comment react"}, 401
    else:
        return {'error': f'There is no comment react with id {comment_react_id}'}, 404
from flask import Blueprint, request, abort
from models.user import User
from models.post_react import PostReact
from schemas.post_react_schema import PostReactSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


post_reacts_bp = Blueprint('post_reacts', __name__, url_prefix='/posts/<int:post_id>/post_reacts')

@post_reacts_bp.route('/', methods=['GET'])
@jwt_required()
def read_post_reacts(post_id):
    stmt = select(PostReact).where(PostReact.post_id == post_id)
    post_reacts = db.session.scalars(stmt)
    return PostReactSchema(many=True).dump(post_reacts)


@post_reacts_bp.route('/<int:post_react_id>', methods=['GET'])
@jwt_required()
def read_post_react(post_id, post_react_id):
    stmt = select(PostReact).where(PostReact.id == post_react_id)
    post_react = db.session.scalar(stmt)

    if post_react:
        return PostReactSchema().dump(post_react)
    else:
        return {'error': f'There is no post react with id {post_react_id}'}, 404


@post_reacts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post_react(post_id):
    post_react_data = PostReactSchema().load(request.json)

    post_react = PostReact(
        type=post_react_data.get('type'),
        date_time=datetime.now(),
        user_id=get_jwt_identity(),
        post_id=post_id
    )

    db.session.add(post_react)
    db.session.commit()
    return PostReactSchema().dump(post_react), 201


@post_reacts_bp.route('/<int:post_react_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post_react(post_id, post_react_id):
    post_react_data = PostReactSchema().load(request.json)

    stmt = select(PostReact).where(PostReact.id == post_react_id)
    post_react = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if post_react:
        if get_jwt_identity() == post_react.user_id or jwt_user.is_admin == True:
            post_react.type = post_react_data.get('type') or post_react.type
            db.session.commit()
            return PostReactSchema().dump(post_react)
        else:
            return {'error': "You are not permitted to update this post react"}, 401
    else:
        return {'error': f'There is no post react with id {post_react_id}'}, 404


@post_reacts_bp.route('/<int:post_react_id>', methods=['DELETE'])
@jwt_required()
def delete_post_react(post_id, post_react_id):
    stmt = select(PostReact).where(PostReact.id == post_react_id)
    post_react = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if post_react:
        if get_jwt_identity() == post_react.user_id or jwt_user.is_admin == True:
            db.session.delete(post_react)
            db.session.commit()
            return {'message': f'Post react {post_react.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this post react"}, 401
    else:
        return {'error': f'There is no post react with id {post_react_id}'}, 404
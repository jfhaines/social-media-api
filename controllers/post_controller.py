from flask import Blueprint, request, abort
from models.user import User
from models.post import Post
from schemas.user_schema import UserSchema
from schemas.post_schema import PostSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils import retrieve_resource_by_id, add_resource_to_db, confirm_authorisation, check_authentication


posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


@posts_bp.route('/', methods=['GET'])
@jwt_required()
def read_posts():
    check_authentication()
    stmt = select(Post)
    posts = db.session.scalars(stmt)
    return PostSchema(many=True).dump(posts)


@posts_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def read_post(post_id):
    check_authentication()
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    return PostSchema().dump(post)


@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    check_authentication()
    post_data = PostSchema(exclude=['user_id']).load(request.json)
    post = Post(
        title=post_data.get('title'),
        text=post_data.get('text'),
        date_time=datetime.now(),
        user_id=get_jwt_identity()
    )
    db.session.add(post)
    db.session.commit()
    return PostSchema().dump(post), 201


@posts_bp.route('/<int:post_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(post_id):
    check_authentication()
    post_data = PostSchema().load(request.json, partial=True)
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    confirm_authorisation(post, action='update', resource_type='post')
    post.title = post_data.get('title') or post.title
    post.text = post_data.get('text') or post.text
    db.session.commit()
    return PostSchema().dump(post)


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    check_authentication()
    post = retrieve_resource_by_id(post_id, model=Post, resource_type='post')
    confirm_authorisation(post, action='delete', resource_type='post')
    db.session.delete(post)
    db.session.commit()
    return {'message': f'Post {post.id} deleted successfully'}

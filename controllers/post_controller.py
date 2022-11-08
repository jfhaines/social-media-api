from flask import Blueprint, request, abort
from models.user import User
from models.post import Post
from schemas.user_schema import UserSchema
from schemas.post_schema import PostSchema
from init import db, bcrypt
from datetime import date, timedelta, datetime
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['GET'])
@jwt_required()
def read_posts():
    stmt = select(Post)
    posts = db.session.scalars(stmt)
    return PostSchema(many=True).dump(posts)


@posts_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def read_post(post_id):
    stmt = select(Post).where(Post.id == post_id)
    post = db.session.scalar(stmt)

    if post:
        return PostSchema().dump(post)
    else:
        return {'error': f'There is no post with id {post_id}'}, 404


@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    post_data = PostSchema().load(request.json)

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
    post_data = PostSchema().load(request.json)

    stmt = select(Post).where(Post.id == post_id)
    post = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if post:
        if get_jwt_identity() == post.user_id or jwt_user.is_admin == True:
            post.title = post_data.get('title') or post.title
            post.text = post_data.get('text') or post.text
            db.session.commit()
            return PostSchema().dump(post)
        else:
            return {'error': "You are not permitted to update this post"}, 401
    else:
        return {'error': f'There is no post with id {post_id}'}, 404


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    stmt = select(Post).where(Post.id == post_id)
    post = db.session.scalar(stmt)

    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if post:
        if get_jwt_identity() == post.user_id or jwt_user.is_admin == True:
            db.session.delete(post)
            db.session.commit()
            return {'message': f'Post {post.id} deleted successfully'}
        else:
            return {'error': "You are not permitted to delete this post"}, 401
    else:
        return {'error': f'There is no post with id {post_id}'}, 404
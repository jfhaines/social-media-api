from models.post import Post
from models.user import User
from models.friendship import Friendship
from sqlalchemy import select
from custom_errors import HttpError
from init import db
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError


def retrieve_resource_by_id(resource_id, model, resource_type):
    stmt = select(model).where(model.id == resource_id)
    resource = db.session.scalar(stmt)
    check_resouce_exists(resource, resource_type, resource_id)
    return resource


def confirm_authorisation(resource, action, resource_type):
    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if isinstance(resource, User):
        resource_user_id = resource.id
    elif isinstance(resource, Friendship):
        resource_user_id = [resource.user1_id, resource.user2_id]
    else:
        resource_user_id = resource.user_id
    
    if type(resource_user_id) is list:
        is_resource_owner = jwt_user.id == resource_user_id[0] or jwt_user.id == resource_user_id[1]
    else:
        is_resource_owner = jwt_user.id == resource_user_id
    is_admin = jwt_user.is_admin

    if action == 'delete' and (is_resource_owner or is_admin):
            return
    elif action == 'update' and (is_resource_owner):
            return
    else:
        raise HttpError(401, f'You are not authorised to {action} this {resource_type}.')


def check_resouce_exists(query_result, resource_type, resource_id):
    if not query_result:
        raise HttpError(404, f'A {resource_type} with id {resource_id} does not exist')


def add_resource_to_db(resource=None, constraint_errors_config=[]):
    try:
        if resource:
            db.session.add(resource)
        db.session.commit()
    except IntegrityError as err:
        constraint_info = []
        for i in range(0, len(constraint_errors_config)):
            store = {}
            store['name'] = constraint_errors_config[i][0]
            store['http_status'] = constraint_errors_config[i][1]
            store['err_message'] = constraint_errors_config[i][2]
            constraint_info.append(store)
        for constraint in constraint_info:
            if err.orig.diag.constraint_name == constraint['name']:
                raise HttpError(constraint['http_status'], constraint['err_message'])

def check_authentication():
    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)
    if not jwt_user:
        raise HttpError(401, 'User with ID in JSON Web Token no longer exists.')

def is_child(parent, child, id_str):
    if type(id_str) is str and parent.id == getattr(child, id_str):
        return
    elif type(id_str) is list and (parent.id == getattr(child, id_str[0]) or parent.id == getattr(child, id_str[1])):
        return
    else:
        parent_name = (parent.__tablename__[0:-1] if parent.__tablename__[-1] == 's' else parent.__tablename__).replace('_', ' ')
        child_name = (child.__tablename__[0:-1] if child.__tablename__[-1] == 's' else child.__tablename__).replace('_', ' ').capitalize()
        raise HttpError(400, f'{child_name} with id {child.id} does not belong to {parent_name} with id {parent.id}.')
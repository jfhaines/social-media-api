from models.post import Post
from models.user import User
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


def confirm_authorisation(query_result, action, resource_type):
    stmt = select(User).where(User.id == get_jwt_identity())
    jwt_user = db.session.scalar(stmt)

    if action == 'delete':
        if get_jwt_identity() == query_result.user_id or jwt_user.is_admin == True:
            return
    elif action == 'update':
        if get_jwt_identity() == query_result.user_id:
            return
    else:
        raise HttpError(401, f'You are not authorised to {action} this {resource_type}.')

def check_resouce_exists(query_result, resource_type, resource_id):
    if not query_result:
        raise HttpError(404, f'{resource_type} with id {resource_id} does not exist')

def add_resource_to_db(resource=None, constraint_errors_config=[]):
    try:
        if resource:
            db.session.add(resource)
        db.commit()
    except IntegrityError as err:
        constraint_info = []
        for i in range(0, len(constraint_errors_config)):
            store = {}
            store['name'] = constraint_errors_config[i][0]
            store['http_status'] = constraint_errors_config[i][1]
            store['err_message'] = constraint_errors_config[i][2]
            constraint_info.append(store)
        for constraint in constraint_info:
            if err.orig.diag.constaint_name == constraint['name']:
                raise HttpError(constraint['http_status'], constraint['err_message']) 


    except IntegrityError as err:
        if err.orig.diag.sqlstate == '23505':
            constraint = err.orig.diag.constraint_name
            table = ''.join(constraint.split('_')[1:-1])
            return {'error': f'You need to enter a unique value for {table}.'}, 409
        elif err.orig.diag.constraint_name == 'valid_dob_cc':
            return {'error': 'You cannot enter a date of birth that is in the future.'}
        else:
            return {'error': f'Cannot register new user, violated constraint "{err.orig.diag.constraint_name}"'}
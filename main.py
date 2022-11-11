from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.auth_controller import auth_bp
from controllers.user_controller import users_bp
from controllers.post_controller import posts_bp
from controllers.comment_controller import comments_bp
from controllers.post_react_controller import post_reacts_bp
from controllers.comment_react_controller import comment_reacts_bp
from controllers.friendship_controller import friendships_bp
from cli_commands import db_commands
from marshmallow.exceptions import ValidationError
from custom_errors import HttpError
import os


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error_handler(err):
        errors = {}
        for k, v in list(err.messages.items()):
            message_store = []
            for subitem in v:
                message_store.append(subitem)
            errors['column'] = k
            errors['message'] = ' '.join(message_store)
        return {'error': errors}, 400
    
    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'{err} is a required field.'}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(HttpError)
    def custom_http_error(err):
        return {'error': err.message}, err.code

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(post_reacts_bp)
    app.register_blueprint(comment_reacts_bp)
    app.register_blueprint(friendships_bp)

    return app
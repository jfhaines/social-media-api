from flask import Flask
from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    return app
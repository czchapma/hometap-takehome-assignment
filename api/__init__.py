from flask import Flask
from os import environ

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    from . import api
    app.register_blueprint(api.bp)
    return app

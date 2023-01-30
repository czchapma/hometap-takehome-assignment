from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    # TODO: move this to env varaible for production
    app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'
    from . import api
    app.register_blueprint(api.bp)
    return app

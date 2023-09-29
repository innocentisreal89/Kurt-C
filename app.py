from os import path
from flask import Flask, jsonify
from config.config import config_dict
from model.url import Url
from model.user import User
from db import db
from extension import cache, limiter
from auth.auth import blp as UserBlueprint
from urls.views import blp as UrlBlueprint
from dashboard.dashboard import blp as DashboardBlueprint
# from resources.user import blp as UserBlueprint
from flask_migrate import Migrate
from flask_login import LoginManager



def create_app(config=config_dict['dev']):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager = LoginManager(app)

    migrate = Migrate(app, db)
    
    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))
    
    cache.init_app(app)

    limiter.init_app(app)

    app.register_blueprint(UserBlueprint,url_prefix='/auth')
    app.register_blueprint(UrlBlueprint,url_prefix='/url_shortener')
    app.register_blueprint(DashboardBlueprint)
    
    

    # @app.shell_context_processor
    # def make_shell_context():
    #     return {
    #         'db':db,
    #         'Url':Url,
    #         'User':User
          
    #     }
           

    if not path.exists('config/' + 'db.sqlite3'):
       with app.app_context():
           db.create_all()
           print("Created Database!")

    
    return app



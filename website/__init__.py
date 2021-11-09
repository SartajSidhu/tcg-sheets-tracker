from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from os import path

#db = SQLAlchemy()
#DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sartaj is best'
    #app.config['SERVER_NAME'] = 'localhost:5000'
    #app.config['SQLAlCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #db.init_app(app)



    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app

from os import path

from flask import Flask

from routes import blueprints
from models import db


class AppConfig:
    use_sqlite = True
    reset_db = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_path = path.abspath('beanstock.db')
        return 'sqlite:///' + db_path


config = AppConfig()

application = Flask(__name__)
application.config.from_object(config)
db.init_app(application)

for blueprint in blueprints:
    application.register_blueprint(blueprint)

if config.reset_db:
    with application.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    application.run()

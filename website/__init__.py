from flask import Flask
from flask_login import LoginManager
from .data.users import User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'signumisthebestgusinthewholeuniverse'


    from .views import views
    from .auth import auth
    from .forms import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    from .data import db_session

    db_session.global_init("website/db/shop.db")

    login_manager = LoginManager()
    login_manager.init_app(app)

    # ищем пользователя
    @login_manager.user_loader
    def load_user(id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(int(id))

    return app

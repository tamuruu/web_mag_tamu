from flask import Flask, abort
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_required

from .data.users import User


class Admin_Go_Back(AdminIndexView):
    @login_required
    @expose('/')
    def go_home(self):
        return self.render('admin/index.html')

class Any_Page_View(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('main/index.html')

class Controller(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'name', 'price', 'stock', 'description')

    def is_accessible(self):
        if current_user.is_admin:
            return current_user.is_authenticated
        else:
            return abort(404)

    def not_auth(self):
        return abort(404)


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

    admin_page = Admin(name='Маркет', template_mode='bootstrap4', index_view=Admin_Go_Back())
    admin_page.init_app(app)
    from .data.add_product import AddProduct
    db_sess = db_session.create_session()
    admin_page.add_view(Controller(AddProduct, db_sess))
    admin_page.add_view(Any_Page_View(name='В магазин'))

    # ищем пользователя
    @login_manager.user_loader
    def load_user(id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(int(id))

    return app

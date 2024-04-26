from flask import Flask, abort
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_required

from .data.categories import Categories
from .data.users import User

# кнопка хоум в админке
class Admin_Go_Back(AdminIndexView):
    @login_required
    @expose('/')
    def go_home(self):
        return self.render('admin/index.html')


# кнопка в магазин в админке
class Any_Page_View(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('main/index.html')

# показатель айди в админке
class Show_ID(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list


# проверка доступа в админку
class Controller(Show_ID):
    # какие колонки показывать в бд products
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

    # регистрация блупринтов
    from .views import views
    from .auth import auth
    from .forms import admin
    from .catalog import catalog
    from .cart import cart
    from .favourites import fav
    from .show_products import cards

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(catalog, url_prefix='/')
    app.register_blueprint(cart, url_prefix='/')
    app.register_blueprint(fav, url_prefix='/')
    app.register_blueprint(cards, url_prefix='/')

    # подключение базы данных
    from .data import db_session
    from .data.categories import Categories

    db_session.global_init("website/db/shop.db")

    db_sess = db_session.create_session()

    login_manager = LoginManager()
    login_manager.init_app(app)

    # подключение админки
    admin_page = Admin(name='Маркет', template_mode='bootstrap4', index_view=Admin_Go_Back())
    admin_page.init_app(app)
    from .data.add_product import AddProduct
    from .data.categories_products import Categories_Products
    db_sess = db_session.create_session()
    admin_page.add_view(Controller(AddProduct, db_sess))
    admin_page.add_view(Show_ID(Categories, db_sess))
    admin_page.add_view(ModelView(Categories_Products, db_sess))
    admin_page.add_view(Any_Page_View(name='В магазин'))

    # ищем пользователя
    @login_manager.user_loader
    def load_user(id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(int(id))

    return app

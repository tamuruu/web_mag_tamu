import os
import secrets

from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, validators
from werkzeug.utils import secure_filename


from .data import db_session
from .data.add_product import AddProduct
from .data.cart import Cart
from .data.categories import Categories
from .data.favourites import Favourites
from .data.users import User
views = Blueprint('views', __name__)


class ProfileForm(FlaskForm):
    name = StringField('Имя', validators=[validators.DataRequired()])
    surname = StringField('Фамилия')
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    photo = FileField('Фото профиля')




@views.route('/')
def home():
    # секции в каталоге
    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address


    # отображение картинки в карточку
    text = db_sess.query(AddProduct).all()
    spi = []
    for i in text:
        image_file1 = url_for('static', filename=f'products_img/{i.id}/{i.image1}')
        image_file2 = url_for('static', filename=f'products_img/{i.id}/{i.image2}')
        image_file3 = url_for('static', filename=f'products_img/{i.id}/{i.image3}')

        spi.append([i.id, i.name, i.price, i.discount, i.stock, i.description, image_file1, True])
    try:
        cart = db_sess.query(Cart).filter(Cart.user_id == current_user.id).all()
        cart_list = []
        for i in cart:
            cart_list.append(i.product_id)

        fav = db_sess.query(Favourites).filter(Favourites.user_id == current_user.id).all()
        fav_list = []
        for i in fav:
            fav_list.append(i.product_id)

        return render_template('home.html', user=current_user, sp=spi, catalog_list=catalog_list, cart_list=cart_list,
                               fav_list=fav_list)
    except Exception:
        return render_template('home.html', user=current_user, sp=spi, catalog_list=catalog_list)


@views.route('/search')
def search():
    query = request.args.get('query')
    db_sess = db_session.create_session()
    text = db_sess.query(AddProduct).filter(AddProduct.name.ilike(f'%{query}%')).all()
    spi = []
    for i in text:
        files = []
        di = os.path.join(current_app.root_path, 'static', 'products_img', str(i.id))
        if not os.path.exists(di):
            os.makedirs(di)
        files += os.listdir(di)
        spi.append({
            'id': i.id,
            'name': i.name,
            'price': i.price,
            'discount': i.discount,
            'stock': i.stock,
            'description': i.description,
            'images': [f'/static/products_img/{i.id}/{file}' for file in files],
        })

    return render_template('search_results.html', user=current_user, products=spi)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = ProfileForm(obj=current_user)
    db_sess = db_session.create_session()
    filename = db_sess.query(User).filter(User.id == current_user.id).first().avatar

    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address

    return render_template('profile.html', form=form, user=current_user, catalog_list=catalog_list, image=filename,)


@views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(current_user)
            if 'photo' in request.files:
                photo = request.files['photo']
                random_hex = secrets.token_hex(16)
                _, format = os.path.splitext(photo.filename)
                filename = random_hex + format
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.id == current_user.id).first()
                old_photo = user.avatar
                os.remove(os.path.join(current_app.root_path, 'static', 'avatars', old_photo))
                photo.save(os.path.join(current_app.root_path, 'static', 'avatars', filename))
                user.avatar = filename
                db_sess.commit()

            # сохраняем изменения пользователя в бд

            # кидаем пользователя на страницу профиля после сохранения
                return redirect(url_for('views.user_profile'))
    return render_template('edit_profile.html', form=form, user=current_user)

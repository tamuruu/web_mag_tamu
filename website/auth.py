from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import login_user, login_required, current_user, logout_user

from .data.users import User
from .data import db_session
from .data.categories import Categories


auth = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password1 = PasswordField(validators=[DataRequired()])
    password2 = PasswordField(validators=[DataRequired()])


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # формирование списка каталога
    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address

    if request.method == 'POST':
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user:
                if check_password(user.hashed_password, form.password.data):
                    #запоминаем, что пользователь зарегался
                    login_user(user, remember=True)
                    print(current_user)
                    return redirect('/')
                else:
                    flash('Неверный пароль', category='error')
            else:
                flash('Такого пользователя не существует')
    return render_template('login.html', form=form, user=current_user, catalog_list=catalog_list)


# разлогиниваем пользователя и переносим его в форму входа
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def set_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_out():
    form = SignUpForm()

    # формирование каталога
    db_sess = db_session.create_session()
    catalog = db_sess.query(Categories).all()
    catalog_list = {}
    for i in catalog:
        catalog_list[i.name] = i.address

    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    email = request.form.get('email')
    name = request.form.get('name')
    surname = request.form.get('surname')
    if request.method == 'POST':
        if password1 != password2:
            print(str(form.password1), str(form.password2))
            flash('Пароли не совпадают', category='error')
        elif db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Такой пользователь уже существует')
        else:
            if form.validate_on_submit():
                new_user = User(
                    name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    hashed_password=set_password(form.password1.data)
                )
                db_sess.add(new_user)
                db_sess.commit()
                return redirect('/login')
    return render_template('sign_up.html', form=form, user=current_user, catalog_list=catalog_list)


from flask import Blueprint, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from .data.users import User
from .data import db_session

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
    db_sess = db_session.create_session()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user:
                if check_password(user.hashed_password, form.password.data):
                    return redirect('/success')
                else:
                    flash('Неверный пароль', category='error')
            else:
                flash('Такого пользователя не существует')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    return '<p>logout</p>'


def set_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_out():
    form = SignUpForm()
    db_sess = db_session.create_session()
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
    return render_template('sign_up.html', form=form)

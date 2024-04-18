from flask import request, redirect, render_template, Blueprint
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, TextAreaField, validators
from sqlalchemy import desc
from .data import db_session
from .data.add_product import AddProduct
from .utils import save_picture

admin = Blueprint('admin', __name__)

class AddProducts(Form):
    name = StringField('Название', [validators.DataRequired()])
    price = IntegerField('Цена', [validators.DataRequired()])
    discount = IntegerField('Скидка', default=0)
    stock = IntegerField('Количество', [validators.DataRequired()])
    description = TextAreaField('Описание', [validators.DataRequired()])
    colors = TextAreaField('Цвета', [validators.DataRequired()])

    image1 = FileField('Фото 1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image2 = FileField('Фото 2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image3 = FileField('Фото 3', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])


@admin.route('/addproduct', methods=['POST', 'GET'])
def add_product():
    form = AddProducts()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        discount = request.form['discount']
        stock = request.form['stock']
        description = request.form['description']
        image1 = request.files['image1']
        image2 = request.files['image2']
        image3 = request.files['image3']
        previous_id = db_sess.query(AddProduct).order_by(desc(AddProduct.id)).first().id
        picture_files = save_picture([image1, image2, image3], id=previous_id + 1)


        product = AddProduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            description=description,
            image1=picture_files[0] if image1 else 'image.jpg',
            image2=picture_files[1] if image2 else 'image.jpg',
            image3=picture_files[2] if image3 else 'image.jpg')

        try:
            db_sess.add(product)
            db_sess.commit()
            return redirect('/')
        except Exception as e:
            return f'Произошла ошибка: {str(e)}'

    else:
        form = AddProducts(request.form)
        return render_template('add_product.html', form=form)

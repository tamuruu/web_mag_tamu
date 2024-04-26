from flask import Blueprint, render_template, request, redirect
import sqlite3
import os.path
import sqlite3
from flask_login import current_user
from .data.users import User

cards = Blueprint('cards', __name__)


@cards.route('/show/<id>', methods=['GET', 'POST'])
def main(id):
    if request.method == 'POST':
        Otziv = request.form.get('Login')  # Запрашива отзыв и оценку
        Ocenka = request.form.get('oc')
        if Otziv:  # Если написали отзыв
            with open('website/static/otzivi/otzivi.txt', mode='a', encoding='utf-8') as f:
                otz = str(id) + ' // ' + str(
                    Otziv + Ocenka + '\n')  # Записываю отзыв и оценку. В начале строки записываю id товара
                f.write(otz)
                f.close()
        return redirect(f'/show/{id}')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "db/shop.db")
    with open('website/static/otzivi/otzivi.txt', mode='r', encoding='utf-8') as file:
        all_otz = file.readlines()
        otzivi_etogo_tovara = []
        for otz in all_otz:
            if otz[0] == str(id):
                otzivi_etogo_tovara.append(otz[5:])  # Выбираю отзывы именно для этого товара
        file.close()
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        zap = f"SELECT * from 'product' WHERE id='{str(id)}'"
        for i in cursor.execute(zap):
            text = i
            print(text)
    return render_template('full_info_about_product.html', item=text, user=current_user, otzivs=otzivi_etogo_tovara)

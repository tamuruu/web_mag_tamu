import os
import secrets

from PIL import Image
from flask import current_app


def save_picture(images, id):
    # определяю папку в которой будут лежать картинки
    full_path = os.path.join(current_app.root_path, 'static', 'products_img', f'{id}')
    pictures_titles = [] # список с названиями картинок
    for image in images:
        if image:
            #генерирую название, чтобы имена картинок не повторялись
            random_hex = secrets.token_hex(16)
            # получаю старое название картинки, оно нам не надо, и формат картинки
            _, format = os.path.splitext(image.filename)
            # объединяю новоя название и формат картинки
            picture_name = random_hex + format

            if not os.path.exists(full_path):
                os.mkdir(full_path)

            picture_path = os.path.join(full_path, picture_name)
            # сохраняем картинку
            im = Image.open(image)

            output_size = (200, 200)
            im.thumbnail(output_size)

            im.save(picture_path)
            pictures_titles.append(picture_name)
        else:
            pictures_titles.append(None)
    return pictures_titles

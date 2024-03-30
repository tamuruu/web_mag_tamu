from flask import Flask, request, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return """<!doctype html>
                    <html lang="en">
                      <head>
                        <link rel="stylesheet" href="static/fonts/st.css">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>МФото</title>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
                      </head>
                      <body>
                      <header class="p-3 bg-dark text-white">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
          <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap"><use xlink:href="#bootstrap"/></svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li><a href="#" class="nav-link px-2 text-secondary">Главная</a></li>
          <li><a href="#" class="nav-link px-2 text-white">Характеристики</a></li>
          <li><a href="#" class="nav-link px-2 text-white">Цены</a></li>
          <li><a href="#" class="nav-link px-2 text-white">Отправить отзыв</a></li>
          <li><a href="#" class="nav-link px-2 text-white">О нас</a></li>
        </ul>

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
          <input type="search" class="form-control form-control-dark" placeholder="Поиск..." aria-label="Search">
        </form>

        <div class="text-end">
          <button type="button" class="btn btn-outline-light me-2">Войти</button>
          <button type="button" class="btn btn-warning">Регистрация</button>
        </div>
      </div>
    </div>
  </header>
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
                      </body>
                    </html>"""



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

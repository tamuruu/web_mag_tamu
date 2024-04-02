from website import create_app
from website.data import db_session

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
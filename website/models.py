import os.path
import sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db/shop.db")
with sqlite3.connect(db_path) as db:
    cursor = db.cursor()
    print('2')
    zap = "SELECT * from 'product'"
    print('3')
    for i in cursor.execute(zap):
        print(i)

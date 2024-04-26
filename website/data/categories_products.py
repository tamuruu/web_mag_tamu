import sqlalchemy

from .db_session import SqlAlchemyBase


# база данных, которая связывает продукты и категориями в каталоге
class Categories_Products(SqlAlchemyBase):
    __tablename__ = 'categories-products'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    categori_id = sqlalchemy.Column(sqlalchemy.Integer)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)

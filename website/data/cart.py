import sqlalchemy

from .db_session import SqlAlchemyBase


# база данных, которая хранит информацию о продуктах в корзине у конкретного пользователя
class Cart(SqlAlchemyBase):
    __tablename__ = 'cart'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    amount = sqlalchemy.Column(sqlalchemy.Integer)

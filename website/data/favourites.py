import sqlalchemy

from .db_session import SqlAlchemyBase


class Favourites(SqlAlchemyBase):
    __tablename__ = 'favourites'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)

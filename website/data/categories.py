import sqlalchemy
from .db_session import SqlAlchemyBase, create_session
from datetime import datetime


# база данных с категориями в каталоге
class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(80), nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String(80), nullable=False)



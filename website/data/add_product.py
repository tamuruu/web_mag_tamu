import sqlalchemy
from .db_session import SqlAlchemyBase
from datetime import datetime


class AddProduct(SqlAlchemyBase):
    __tablename__ = 'product'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(80), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    discount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    stock = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    pub_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.utcnow)

    image1 = sqlalchemy.Column(sqlalchemy.String(150), nullable=True, default='None')
    image2 = sqlalchemy.Column(sqlalchemy.String(150), nullable=True, default='None')
    image3 = sqlalchemy.Column(sqlalchemy.String(150), nullable=True, default='None')

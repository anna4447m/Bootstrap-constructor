import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

class Object(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'object'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    program_title = sqlalchemy.Column(sqlalchemy.String)
    title_for_human = sqlalchemy.Column(sqlalchemy.String)
    pattern = sqlalchemy.Column(sqlalchemy.String)
    properties = sqlalchemy.Column(sqlalchemy.String)
    insert_indexes = sqlalchemy.Column(sqlalchemy.String)
    image_name = sqlalchemy.Column(sqlalchemy.String)
    # user = orm.relation('User')



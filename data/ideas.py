import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Idea(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'ideas'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    component_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("object.id"))
    idea_name = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    component_parameters_values = sqlalchemy.Column(sqlalchemy.String)
    component_text = sqlalchemy.Column(sqlalchemy.String)
    users = orm.relation('User')
    object = orm.relation('Object')
import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Property(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'property'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title_for_human = sqlalchemy.Column(sqlalchemy.String)
    css_name = sqlalchemy.Column(sqlalchemy.String)
    # user = orm.relation('User')

    def __repr__(self):
        return '<News> '+str(self.id) +' '+ self.title +' '+ self.content
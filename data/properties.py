import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Property(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'property'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    program_title = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return '<Property> ' + str(self.id) + ' ' + self.program_title
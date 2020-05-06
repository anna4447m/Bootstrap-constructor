import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Object(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'object'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True)
    program_title = sqlalchemy.Column(sqlalchemy.String, index=True, primary_key=True)
    title_for_human = sqlalchemy.Column(sqlalchemy.String)
    image_name = sqlalchemy.Column(sqlalchemy.String)
    component_parameters = sqlalchemy.Column(sqlalchemy.String)
    component_text = sqlalchemy.Column(sqlalchemy.String)

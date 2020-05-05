import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Property_values(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'properties_values'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    prop_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("property.id"))
    program_title = sqlalchemy.Column(sqlalchemy.String)
    title_for_human = sqlalchemy.Column(sqlalchemy.String)
    property = orm.relation('Property')

    def __repr__(self):
        return '<Property_values> '+str(self.id) +' '+ self.prop_id +' '+ self.program_title +' '+ self.title_for_human
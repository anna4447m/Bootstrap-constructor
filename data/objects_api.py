import flask
from flask import jsonify
from data import db_session

from data.objects import Object
from data.properties import Property


blueprint = flask.Blueprint('objects_api', __name__,
                            template_folder='templates')

@blueprint.route('/objects')
def get_objects():
    session = db_session.create_session()
    obj = session.query(Object).all()
    return jsonify(
        {
            'object':
                [item.to_dict(only=('program_title', 'title_for_human', 'image_name'))
                 for item in obj]
        }
    )


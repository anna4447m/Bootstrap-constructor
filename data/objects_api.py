import flask
from flask import jsonify
from data import db_session

from data.objects import Object

blueprint = flask.Blueprint('objects_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/objects')
def get_objects():
    session = db_session.create_session()
    obj = session.query(Object).all()
    return jsonify(
        {
            'object':
                [item.to_dict(only=('id', 'program_title', 'title_for_human', 'image_name',
                                    'component_parameters', 'component_text'))
                 for item in obj]
        }
    )


@blueprint.route('/api/objects/<string:obj_name>',  methods=['GET'])
def get_one_object(obj_name):
    session = db_session.create_session()
    obj = session.query(Object).get(obj_name)
    if not obj:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'object': obj.to_dict(only=('id', 'program_title', 'title_for_human', 'image_name',
                                        'component_parameters', 'component_text'))
        }
    )

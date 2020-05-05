import flask
from flask import jsonify
from data import db_session

from data.prop_values import Property_values
from data.properties import Property

blueprint = flask.Blueprint('prop_api', __name__,
                            template_folder='templates')

@blueprint.route('/properties')
def get_properties():
    session = db_session.create_session()
    prop = session.query(Property).all()
    return jsonify(
        {
            'properties':
                [item.to_dict(only=('id', 'program_title'))
                 for item in prop]
        }
    )

@blueprint.route('/properties/<int:pr_id>',  methods=['GET'])
def get_prop_values(pr_id):
    session = db_session.create_session()
    prop_val = session.query(Property_values).all()
    if not prop_val:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'prop_values':
                [item.to_dict(only=('program_title', 'title_for_human'))
                 for item in prop_val]
        }
    )

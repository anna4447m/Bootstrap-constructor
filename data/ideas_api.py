import flask
from flask import jsonify
from data import db_session

from data.ideas import Idea

blueprint = flask.Blueprint('ideas_api', __name__,
                            template_folder='templates')

@blueprint.route('/ideas')
def get_ideas():
    session = db_session.create_session()
    idea = session.query(Idea).all()
    return jsonify(
        {
            'ideas':
                [item.to_dict(only=('user_id', 'component_id', 'idea_name', 'created_date',
                                    'component_parameters_values', 'component_text'))
                 for item in idea]
        }
    )

@blueprint.route('/ideas/<int:idea_id>',  methods=['GET'])
def get_one_idea(idea_id):
    session = db_session.create_session()
    idea = session.query(Idea).get(idea_id)
    if not idea:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'idea': idea.to_dict(only=('user_id', 'component_id', 'idea_name', 'created_date',
                                    'component_parameters_values', 'component_text'))
        }
    )

@blueprint.route('/ideas/<int:idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    session = db_session.create_session()
    idea = session.query(Idea).get(idea_id)
    if not idea:
        return jsonify({'error': 'Not found'})
    session.delete(idea)
    session.commit()
    return jsonify({'success': 'OK'})

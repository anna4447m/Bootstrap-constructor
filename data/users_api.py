import flask
from flask import jsonify
from data import db_session

from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    user = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('login', 'nickname', 'created_date'))
                 for item in user]
        }
    )


@blueprint.route('/api/users/<string:user_login>',  methods=['GET'])
def get_one_user(user_login):
    session = db_session.create_session()
    user = session.query(User).get(user_login)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('login', 'nickname', 'created_date'))
        }
    )


@blueprint.route('/api/users/<string:user_login>', methods=['DELETE'])
def delete_user(user_login):
    session = db_session.create_session()
    user = session.query(User).get(user_login)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


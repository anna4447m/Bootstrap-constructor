from flask import Flask, render_template, redirect, jsonify
from flask import request, make_response, session, abort
from data import db_session, objects_api, users_api, ideas_api

from data.objects import Object
from data.properties import Property
from data.prop_values import Property_values
from data.users import User
from data.ideas import Idea

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from flask_restful import abort, Api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
def index():
    session = db_session.create_session()
    return 'bootstrap-constructor'

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def main():
    db_session.global_init("db/objects_properties.sqlite")
    app.register_blueprint(objects_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(ideas_api.blueprint)
    app.run(port=8080, host='127.0.0.1')

if __name__ == '__main__':
    main()
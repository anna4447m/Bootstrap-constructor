from flask import Flask, render_template, request, jsonify, redirect, abort, make_response
from requests import get
import os

from data import db_session, objects_api, users_api, ideas_api, prop_api
from data.objects import Object
from data.properties import Property
from data.prop_values import Property_values
from data.users import User
from data.ideas import Idea

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user
from flask_login import login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


params = {}
texts = {}
zamena = '<a'


def string_to_dict(s):
    d = {}
    s = s.replace('}', '').replace('{', '')
    for i in s.split("', '"):
        a = i.split("': '")
        if len(a) == 1:
            a = i.split("': ")
        d[a[0].replace("'", "")] = a[1].replace("'", "").replace(r"\r\n", "\r\n")
    return d


class PropertiesForm(FlaskForm):
    btn_color = SelectField('Цвет', choices=[
        ('blue', 'Синий'),
        ('grey', 'Серый'),
        ('green', 'Зеленый'),
        ('red', 'Красный'),
        ('yellow', 'Желтый'),
        ('griz', 'Бирюзовый'),
        ('white', 'Белый'),
        ('black', 'Черный'),
        ('link', 'Прозрачный')
    ],
                            default="blue")
    color = SelectField('Цвет', choices=[
        ('blue', 'Синий'),
        ('grey', 'Серый'),
        ('green', 'Зеленый'),
        ('red', 'Красный'),
        ('yellow', 'Желтый'),
        ('griz', 'Бирюзовый'),
        ('white', 'Белый'),
        ('black', 'Черный')
    ],
                        default="blue")
    color_alert = SelectField('Цвет', choices=[
        ('blue', 'Синий'),
        ('grey', 'Серый'),
        ('green', 'Зеленый'),
        ('red', 'Красный'),
        ('yellow', 'Желтый'),
        ('griz', 'Бирюзовый'),
        ('white', 'Белый'),
        ('black', 'Черный')
    ],
                        default="blue")
    backdrop = BooleanField('Фон',
                            default=True)
    link_color = BooleanField('Закрашивание ссылки',
                              default=False)
    dagger = BooleanField('Наличие крестика',
                          default=False)
    strips = BooleanField('Наличие полосок',
                          default=False)
    animate = BooleanField('Анимация',
                           default=False)
    all_w = BooleanField('Во всю ширину:',
                         default=False)
    sizing = SelectField('Размер:', choices=[
        ('1', 'Маленький'),
        ('2', 'Обычный'),
        ('3', 'Большой')
    ],
                         default=2)
    condition = SelectField('Состояние:', choices=[
        ('usual', 'Обычное'),
        ('aktive', 'Активное'),
        ('disaktive', 'Неактивное')
    ],
                            default="usual")
    running_value = IntegerField('Значение прогрессбара', validators=[DataRequired()],
                                 default="75")
    heights = IntegerField('Высота прогрессбара', validators=[DataRequired()],
                           default="15")
    submit_p = SubmitField('Применить')


class TextEditorForm(FlaskForm):
    caption_bth = StringField("Надпись на кнопке",
                              default="Главный")
    label_bar = StringField("Лейбл на баре",
                            default="75%")
    text_alert = TextAreaField("Текст уведомления",
                               default="Уведомляем вас о том, что сайт работает успешно!")
    submit_t = SubmitField('Применить')


class RegisterForm(FlaskForm):
    login = StringField('Придумайте логин', validators=[DataRequired()])
    nickname = StringField('Придумайте, как мы к вам будем обращаться', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль ещё раз', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SaveForm(FlaskForm):
    name = StringField('Придумайте назване для идеи, по которому вы потом сможете его узнать',
                       validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class EditSaveForm(FlaskForm):
    name = StringField('Придумайте название для идеи, по которому вы потом сможете его узнать',
                       validators=[DataRequired()])
    submit_save = SubmitField('Сохранить как новую идею')
    submit_edit = SubmitField('Сохранить изменения')


@app.route('/')
@app.route('/index')
def index():
    global params, texts
    komponents = get('http://bootstrap-constructor.herokuapp.com/api/objects').json()
    params = {}
    texts = {}
    return render_template('index.html', komponent=komponents, name='first')


@app.route('/work/<name_object>', methods=['GET', 'POST'])
def work(name_object):
    global params, texts
    s = name_object + '.html'
    form_p = PropertiesForm()
    form_t = TextEditorForm()
    form_s = SaveForm()
    session = db_session.create_session()
    com = session.query(Object).filter(Object.program_title == name_object).first()
    com_text = com.component_text.split(', ')
    com_prop = com.component_parameters.split(', ')
    title = com.title_for_human
    if form_t.submit_t.data:
        texts = {}
        for field in form_t:
            if field.name in com_text:
                texts[field.name] = field.data
    if form_p.submit_p.data:
        params = {}
        for field in form_p:
            if field.name in com_prop:
                i = session.query(Property).filter(Property.program_title == field.name).first()
                if i:
                    i = i.id
                    p = session.query(Property_values).filter(Property_values.prop_id == i,
                                                              Property_values.title_for_human == str(field.data))
                    p = p.first().program_title
                    params[field.name] = p
                else:
                    params[field.name] = str(field.data)
    if not params:
        params = {}
        for field in form_p:
            if field.name in com_prop:
                i = session.query(Property).filter(Property.program_title == field.name).first()
                if i:
                    i = i.id
                    p = session.query(Property_values).filter(Property_values.prop_id == i,
                                                              Property_values.title_for_human == str(field.data))
                    p = p.first().program_title
                    params[field.name] = p
                else:
                    params[field.name] = str(field.data)
    if not texts:
        texts = {}
        for field in form_t:
            if field.name in com_text:
                texts[field.name] = field.data
    for field in form_t:
        if field.name in com_text:
            field.data = texts[field.name]
    for field in form_p:
        if field.name in com_prop:
            i = session.query(Property).filter(Property.program_title == field.name).first()
            if i:
                i = i.id
                p = session.query(Property_values).filter(Property_values.prop_id == i,
                                                          Property_values.program_title == params[field.name])
                p = p.first().title_for_human
                if p == 'False':
                    p = False
            else:
                p = int(params[field.name])
            field.data = p
    if form_s.validate_on_submit():
        idea = Idea()
        idea.user_id = current_user.id
        idea.user = current_user
        idea.component_id = com.id
        idea.object = com
        idea.idea_name = form_s.name.data
        idea.component_parameters_values = str(params)
        idea.component_text = str(texts)
        session.add(idea)
        session.commit()
        return redirect('/ideas')
    return render_template(s, form_p=form_p, form_t=form_t, form_s=form_s, params=params, texts=texts,
                           zamena=zamena, name='two', title=title, edit=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form,
                                   message="Пароли не совпадают", name="form")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', form=form,
                                   message="Такой пользователь уже есть", name="form")
        user = User()
        user.login = form.login.data
        user.nickname = form.nickname.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', form=form, name="form")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/ideas")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, name="form")
    return render_template('login.html', form=form, name="form")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/ideas')
@login_required
def show_ideas():
    global params, texts
    params = {}
    texts = {}
    session = db_session.create_session()
    ideas = session.query(Idea).filter(Idea.user_id == current_user.id).all()
    return render_template('ideas.html', name="ideas", ideas=ideas)


@app.route('/idea_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_idea(id):
    session = db_session.create_session()
    idea = session.query(Idea).filter(Idea.id == id, ((Idea.user_id == 1) | (Idea.user_id == current_user.id))).first()
    if idea:
        session.delete(idea)
        session.commit()
    else:
        abort(404)
    return redirect('/ideas')


@app.route('/work/<name_object>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_idea(name_object, id):
    global params, texts
    session = db_session.create_session()
    idea = session.query(Idea).filter(Idea.id == id, Idea.user_id == current_user.id).first()
    if not idea:
        abort(404)
    if not params:
        params = string_to_dict(idea.component_parameters_values)
        texts = string_to_dict(idea.component_text)
    s = name_object + '.html'
    form_p = PropertiesForm()
    form_t = TextEditorForm()
    form_s = EditSaveForm()
    com = session.query(Object).filter(Object.program_title == name_object).first()
    com_text = com.component_text.split(', ')
    com_prop = com.component_parameters.split(', ')
    title = com.title_for_human
    if form_t.submit_t.data:
        texts = {}
        for field in form_t:
            if field.name in com_text:
                texts[field.name] = field.data
    if form_p.submit_p.data:
        params = {}
        for field in form_p:
            if field.name in com_prop:
                i = session.query(Property).filter(Property.program_title == field.name).first()
                if i:
                    i = i.id
                    p = session.query(Property_values).filter(Property_values.prop_id == i,
                                                              Property_values.title_for_human == str(field.data))
                    p = p.first().program_title
                    params[field.name] = p
                else:
                    params[field.name] = str(field.data)
    for field in form_t:
        if field.name in com_text:
            field.data = texts[field.name]
    for field in form_p:
        if field.name in com_prop:
            i = session.query(Property).filter(Property.program_title == field.name).first()
            if i:
                i = i.id
                p = session.query(Property_values).filter(Property_values.prop_id == i,
                                                          Property_values.program_title == params[field.name])
                p = p.first().title_for_human
                if p == 'False':
                    p = False
            else:
                p = int(params[field.name])
            field.data = p
    if form_s.validate_on_submit():
        if form_s.submit_save.data:
            idea = Idea()
            idea.user_id = current_user.id
            idea.user = current_user
            idea.component_id = com.id
            idea.object = com
            idea.idea_name = form_s.name.data
            idea.component_parameters_values = str(params)
            idea.component_text = str(texts)
            session.add(idea)
            session.commit()
            return redirect('/ideas')
        elif form_s.submit_edit.data:
            idea.user_id = current_user.id
            idea.user = current_user
            idea.component_id = com.id
            idea.object = com
            idea.idea_name = form_s.name.data
            idea.component_parameters_values = str(params)
            idea.component_text = str(texts)
            session.commit()
            return redirect('/ideas')
    form_s.name.data = idea.idea_name
    return render_template(s, form_p=form_p, form_t=form_t, form_s=form_s, params=params, texts=texts,
                           zamena=zamena, name='two', title=title, edit=True)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/objects_properties.sqlite")
    app.register_blueprint(objects_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(ideas_api.blueprint)
    app.register_blueprint(prop_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(port=8080, host='127.0.0.1')
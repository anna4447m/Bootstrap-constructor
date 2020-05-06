from flask import Flask, render_template, request, jsonify
from requests import get

from data import db_session, objects_api, users_api, ideas_api, prop_api
from data.objects import Object
from data.properties import Property
from data.prop_values import Property_values

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
params = {}
texts = {}
zamena = '<a'


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


@app.route('/')
@app.route('/index')
def index():
    global params, texts
    komponents = get('http://localhost:8080/api/objects').json()
    params = {}
    texts = {}
    return render_template('index.html', komponent=komponents, name='first')


@app.route('/work/<name_object>', methods=['GET', 'POST'])
def work(name_object):
    global params, texts
    s = name_object + '.html'
    form_p = PropertiesForm()
    form_t = TextEditorForm()
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
                    params[field.name] = int(field.data)
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
                    params[field.name] = int(field.data)
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
                p = params[field.name]
            field.data = p
    return render_template(s, form_p=form_p, form_t=form_t, params=params, texts=texts, zamena=zamena, name='two', title=title)


if __name__ == '__main__':
    db_session.global_init("db/objects_properties.sqlite")
    app.register_blueprint(objects_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(ideas_api.blueprint)
    app.register_blueprint(prop_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
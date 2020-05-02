from flask import Flask, render_template, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
params = {}
texts = {}
COMPONENT_PARAMETERS = {  # этом можно засунуть в таблицу, где все компоненты, ещё одним столибком. По названию компонента получить кортеж (строчка 173)
    'button': ('btn_color', 'backdrop', 'sizing', 'condition'),
    'alert': ('color', 'link_color', 'dagger'),
    'progress_bar': ('color', 'running_value', 'heights', 'strips', 'animate')
}
COMPONENT_TEXT = {  # и это тоже. По названию копомнента получить кортеж (строчка 172)
    'button': ('caption_bth',),
    'alert': ('text_alert',),
    'progress_bar': ('label_bar',)
}
PROPERTIES = {  # а вот насчет этого не знаю. Во-первых, получить спиоск/кортеж всех свойств (строки 183 и 191), во-вторых - получить рабочее значение свойства по ччп-значению (строки 184 и 192)
    'btn_color': {
        'blue': 'primary',
        'grey': 'secondary',
        'green': 'success',
        'red': 'danger',
        'yellow': 'warning',
        'griz': 'info',
        'white': 'light',
        'black': 'dark',
        'link': 'link'
    },
    'backdrop': {
        True: '',
        False: 'outline-'
    },
    'sizing': {
        '1': ' btn-sm',
        '2': '',
        '3': ' btn-lg',
        '4': ' btn-block'
    },
    'condition': {
        'usual': '',
        'aktive': ' active',
        'disaktive': 'disabled'
    },
    'color': {
        'blue': 'primary',
        'grey': 'secondary',
        'green': 'success',
        'red': 'danger',
        'yellow': 'warning',
        'griz': 'info',
        'white': 'light',
        'black': 'dark'
    },
    'link_color': {
        True: '<a class="alert-link"',
        False: '<a'
    },
    'dagger': {
        True: f'''\n<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>''',
        False: ''
    },
    'strips': {
        True: ' progress-bar-striped',
        False: ''
    },
    'animate': {
        True: ' progress-bar-animated',
        False: ''
    }
}
zamena = '<a'  # это мой костыль, не трогайте пожалуйста :)


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
    backdrop = BooleanField('Фон', default=True)
    link_color = BooleanField('Закрашивание ссылки', default=False)
    dagger = BooleanField('Наличие крестика', default=False)
    strips = BooleanField('Наличие полосок', default=False)
    animate = BooleanField('Анимация', default=False)
    sizing = SelectField('Размер:', choices=[
        ('1', 'Маленький'),
        ('2', 'Обычный'),
        ('3', 'Большой'),
        ('4', 'Во всю ширину')
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
    komponents = {
        "object": [
            {
                "image_name": "button.png",
                "program_title": "button",
                "title_for_human": "Кнопка"
            },
            {
                "image_name": "progress_bar.png",
                "program_title": "progress_bar",
                "title_for_human": "Прогрессбар"
            },
            {
                "image_name": "alert.png",
                "program_title": "alert",
                "title_for_human": "Уведомление"
            }
        ]
    }
    params = {}
    texts = {}
    return render_template('index.html', komponent=komponents)


@app.route('/work/<name_object>', methods=['GET', 'POST'])
def work(name_object):
    global params, texts
    s = name_object + '.html'
    form_p = PropertiesForm()
    form_t = TextEditorForm()
    com_text = COMPONENT_TEXT[name_object]
    com_prop = COMPONENT_PARAMETERS[name_object]
    if form_t.submit_t.data:
        texts = {}
        for field in form_t:
            if field.name in com_text:
                texts[field.name] = field.data
    if form_p.submit_p.data:
        params = {}
        for field in form_p:
            if field.name in com_prop:
                if field.name in PROPERTIES:
                    params[field.name] = PROPERTIES[str(field.name)][field.data]
                else:
                    params[field.name] = int(field.data)
    if not params:
        params = {}
        for field in form_p:
            if field.name in com_prop:
                if field.name in PROPERTIES:
                    params[field.name] = PROPERTIES[str(field.name)][field.data]
                else:
                    params[field.name] = int(field.data)
    if not texts:
        texts = {}
        for field in form_t:
            if field.name in com_text:
                texts[field.name] = field.data
    return render_template(s, form_p=form_p, form_t=form_t, params=params, texts=texts, zamena=zamena)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
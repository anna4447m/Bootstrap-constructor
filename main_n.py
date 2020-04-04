from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    komponents = {
        "object": [
            {
                "image_name": "button.png",
                "program_title": "Button",
                "title_for_human": "Кнопка"
            },
            {
                "image_name": "progress_bar.png",
                "program_title": "Progress_bar",
                "title_for_human": "Прогрессбар"
            },
            {
                "image_name": "alert.png",
                "program_title": "Alert",
                "title_for_human": "Уведомление"
            }
        ]
    }
    return render_template('index.html', komponent=komponents)


@app.route('/work/<name_object>')
def work(name_object):
    return name_object


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
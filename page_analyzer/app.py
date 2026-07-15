import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # Пришлось указать шаблон явно, так как Flask(__name__) определяет приложение и ищет его относительно текущего модуля
    # Указывая явно, начинает смотреть корневую директорию проекта
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()


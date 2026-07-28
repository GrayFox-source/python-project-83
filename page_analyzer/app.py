import os
import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import ConnectionError, RequestException, Timeout

from . import db
from .parser import parse_page
from .url_normalizer import normalize_url

load_dotenv()

def create_app():
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/urls', methods=['POST'])
    def add_url():
        url = request.form.get('url', '').strip()

        if not url or len(url) > 255 or not validators.url(url):
            flash('Некорректный URL', 'danger')
            return render_template('index.html'), 422

        normalized_url = normalize_url(url)

        existing = db.get_url_by_name(normalized_url)
        if existing:
            flash('Страница уже существует', 'info')
            return redirect(url_for('urls_show', url_id=existing[0]), code=303)

        new_id = db.create_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_show', url_id=new_id), code=303)

    @app.route('/urls', methods=['GET'])
    def urls_list():
        urls = db.get_all_urls()
        return render_template('urls.html', urls=urls)

    @app.route('/urls/<int:url_id>')
    def urls_show(url_id):
        url_data = db.get_url_by_id(url_id)
        if not url_data:
            flash('Страница не найдена', 'danger')
            return redirect(url_for('urls_list'), code=303)

        checks = db.get_checks_by_url_id(url_id)
        return render_template('url_show.html', url_data=url_data, checks=checks)

    @app.route('/urls/<int:url_id>/checks', methods=['POST'])
    def create_check(url_id):
        url_record = db.get_url_by_id(url_id)
        if not url_record:
            flash('URL не найден', 'danger')
            return redirect(url_for('urls_list'), code=303)

        url_to_check = url_record[1]

        try:
            parsed_data = parse_page(url_to_check)
            db.create_check(
                url_id=url_id,
                status_code=parsed_data['status_code'],
                h1=parsed_data['h1'],
                title=parsed_data['title'],
                description=parsed_data['description']
            )
            flash('Страница успешно проверена', 'success')
        except (Timeout, ConnectionError):
            flash('Произошла ошибка при проверке', 'danger')
        except RequestException:
            flash('Произошла ошибка при проверке', 'danger')
        except Exception as e:
            print(f"Unexpected error: {e}")
            flash('Произошла ошибка при проверке', 'danger')

        return redirect(url_for('urls_show', url_id=url_id), code=303)

    return app

app = create_app()
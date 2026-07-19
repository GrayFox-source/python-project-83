import os
from datetime import date
from urllib.parse import urlparse
import validators
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from . import db

load_dotenv()

def create_app():
    # Явное указание пути к templates
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

    db.init_db()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            url = request.form.get('url', '').strip()

            if not url:
                flash('Некорректный URL!', 'danger')
                return redirect(url_for('index'), code=303)

            if len(url) > 255:
                flash('URL не должен превышать 255 символов', 'danger')
                return redirect(url_for('index'), code=303)

            if not validators.url(url):
                flash('Некорректный URL!', 'danger')
                return redirect(url_for('index'), code=303)

            # Нормализация url адреса
            parsed = urlparse(url)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}"

            conn = db.get_db_connection()
            try:
                with conn.cursor() as cur:
                    # Проверка на существования URL
                    cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
                    existing = cur.fetchone()

                    if existing:
                        flash('Страница уже существует', 'info')
                        return redirect(url_for('urls_show', url_id=existing[0]), code=303)

                    # Все ок, добавляем
                    cur.execute(
                        "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                        (normalized_url, date.today())
                    )
                    new_id = cur.fetchone()[0]
                conn.commit()
                flash('Страница успешно добавлена', 'success')
                return redirect(url_for('urls_show', url_id=new_id), code=303)
            finally:
                conn.close()

        # Если пришел GET-запрос
        return render_template('index.html')

    @app.route('/urls', methods=['GET'])
    def urls_list():
        conn = db.get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT u.id, u.name, u.created_at, MAX(uc.created_at) as last_check
                        FROM urls u
                                 LEFT JOIN url_checks uc ON u.id = uc.url_id
                        GROUP BY u.id, u.name, u.created_at
                        ORDER BY u.id DESC
                        """)
            urls = cur.fetchall()
        conn.close()
        return render_template('urls.html', urls=urls)

    @app.route('/urls', methods=['POST'])
    def add_url():
        url = request.form.get('url', '').strip()

        if not url:
            flash('Некорректный URL!', 'danger')
            return redirect(url_for('index'), code=303)

        if len(url) > 255:
            flash('URL не должен превышать 255 символов', 'danger')
            return redirect(url_for('index'), code=303)

        if not validators.url(url):
            flash('Некорректный URL!', 'danger')
            return redirect(url_for('index'), code=303)

        parsed = urlparse(url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}"

        conn = db.get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
                existing = cur.fetchone()

                if existing:
                    flash('Страница уже существует', 'info')
                    return redirect(url_for('urls_show', url_id=existing[0]), code=303)

                cur.execute(
                    "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                    (normalized_url, date.today())
                )
                new_id = cur.fetchone()[0]
            conn.commit()
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('urls_show', url_id=new_id), code=303)
        finally:
            conn.close()

    @app.route('/urls/<int:url_id>')
    def urls_show(url_id):
        conn = db.get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s",
                (url_id,)
            )
            url_data = cur.fetchone()

            cur.execute("""
                        SELECT id, status_code, h1, title, description, created_at
                        FROM url_checks
                        WHERE url_id = %s
                        ORDER BY id DESC
                        """, (url_id,))
            checks = cur.fetchall()
        conn.close()

        if not url_data:
            flash('Страница не найдена', 'danger')
            return redirect(url_for('urls_list'), code=303)

        return render_template('url_show.html', url_data=url_data, checks=checks)

    @app.route('/urls/<int:url_id>/checks', methods=['POST'])
    def create_check(url_id):
        conn = db.get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM urls WHERE id = %s", (url_id,))
                url_exists = cur.fetchone()

                if not url_exists:
                    flash('URL не найден', 'danger')
                    return redirect(url_for('urls_list'), code=303)

                cur.execute("""
                            INSERT INTO url_checks (url_id, created_at)
                            VALUES (%s, %s) RETURNING id
                            """, (url_id, date.today()))
            conn.commit()
            flash('Страница успешно проверена', 'success')
            return redirect(url_for('urls_show', url_id=url_id), code=303)
        finally:
            conn.close()

    return app

app = create_app()
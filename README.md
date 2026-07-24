### Hexlet tests and linter status:
[![Actions Status](https://github.com/GrayFox-source/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/GrayFox-source/python-project-83/actions)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=FlexFox-source_python-project-83)
[![Maintainability](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=FlexFox-source_python-project-83)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=bugs)](https://sonarcloud.io/summary/new_code?id=FlexFox-source_python-project-83)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=FlexFox-source_python-project-83)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=FlexFox-source_python-project-83)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=FlexFox-source_python-project-83)

# Анализатор страниц (Page Analyzer)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Deploy](https://img.shields.io/badge/Deploy-Render.com-brightgreen.svg)](https://render.com/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GrayFox-source_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=YOUR_GITHUB_USERNAME_python-project-83)

Веб-приложение для SEO-анализа веб-страниц. Проверяет доступность сайтов и извлекает основные метаданные: заголовки, описания и коды ответов.

## 🚀 Демо

Приложение доступно по адресу: [https://python-project-83-b6xd.onrender.com/](https://python-project-83-b6xd.onrender.com/)

## ⚙️ Возможности

-  Добавление и валидация URL сайтов
-  Проверка доступности сайтов (реальные HTTP-запросы)
-  Извлечение SEO-данных:
  - Код ответа сервера (status code)
  - Заголовок `<h1>`
  - Мета-тег `<title>`
  - Мета-описание `<meta name="description">`
-  История всех проверок с датами
-  Автоматическое усечение длинных значений (до 200 символов + `...`)
-  Обработка ошибок сети и невалидных ответов сервера

## 🛠 Технологический стек

- **Backend:** Python 3.12, Flask 3.0, Gunicorn
- **Database:** PostgreSQL 15, Psycopg 3
- **Frontend:** Bootstrap 5, Jinja2
- **Tools:** UV (менеджер пакетов), BeautifulSoup 4, Requests, Validators, Ruff
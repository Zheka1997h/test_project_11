Django Shop — учебный проект интернет-магазина
Учебный проект интернет-магазина на Django с подключением PostgreSQL, моделями продуктов и категорий, админ-панелью и кастомными командами управления.

🚀 Технологии
Python 3.10+
Django 4.2.7
PostgreSQL — основная база данных
psycopg2-binary — драйвер для PostgreSQL
Pillow — работа с изображениями
ipython — улучшенная интерактивная оболочка
python-dotenv — управление переменными окружения
📁 Структура проекта
Django_Project/ ├── catalog/ │ ├── forms.py ← НОВЫЙ │ ├── views.py ← ОБНОВЛЕН │ ├── urls.py ← ОБНОВЛЕН │ ├── models.py ← без изменений │ ├── admin.py ← без изменений │ ├── management/ │ │ └── commands/populate_db.py ← без изменений │ └── fixtures/ │ ├── categories.json │ ── products.json ├── templates/ │ └── catalog/ │ ├── base.html ← ОБНОВЛЕНО │ ├── menu.html ← НОВЫЙ │ ├── home.html ← ОБНОВЛЕНО │ ├── contacts.html ← без изменений │ ├── product_detail.html ← НОВЫЙ │ └── add_product.html ← НОВЫЙ ├── config/ │ ├── settings.py │ ├── urls.py │ └── wsgi.py ├── static/css/style.css ├── media/products/ ├── requirements.txt └── manage.py

🛠️ Установка и запуск
1. Клонирование репозитория
git clone <url-репозитория>
cd Django_Project


Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

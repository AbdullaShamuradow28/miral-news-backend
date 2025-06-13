# 📰 Miral News Backend

**Miral News Backend** — это серверная часть мобильного Flutter-приложения, предоставляющая API для отображения новостных статей. Построен на **Django** и **Django REST Framework**, использует **SQLite** как базу данных.

---

## 🧩 Возможности

- 🔹 Получение списка статей
- 🔹 Создание, редактирование и удаление статей
- 🔹 Загрузка изображений
- 🔹 JSON API для интеграции с Flutter

---

## ⚙️ Технологии

- Python 3.10+
- Django 4.x
- Django REST Framework
- SQLite (встроено)
- CORS (используется с Flutter)

---

## 🗂️ Структура проекта

miral_news_backend/
├── backend/                # Приложение с логикой статей
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── miral_news_backend/    # Конфигурация проекта
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/                 # Загрузка изображений (Для статей)
├── static/                # Статические файлы
├── bot.py                 # Telegram-бот (пока не запущен)
├── db.sqlite3             # База данных
└── manage.py              # Управление Django

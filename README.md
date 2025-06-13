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

miral_news_backend/ <br/>
├── backend/                # Приложение с логикой статей <br/>
│   ├── admin.py <br/>
│   ├── apps.py <br/>
│   ├── models.py <br/>
│   ├── serializers.py <br/>
│   ├── tests.py<br/>
│   ├── urls.py<br/>
│   └── views.py<br/>
│<br/>
├── miral_news_backend/    # Конфигурация проекта<br/>
│   ├── settings.py<br/>
│   ├── urls.py<br/>
│   ├── asgi.py<br/>
│   └── wsgi.py<br/>
│<br/>
├── media/                 # Загрузка изображений (Для статей)<br/>
├── static/                # Статические файлы<br/>
├── bot.py                 # Telegram-бот (пока не запущен)<br/>
├── db.sqlite3             # База данных<br/>
└── manage.py              # Управление Django<br/>

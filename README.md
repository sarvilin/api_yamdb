# Проект YaMDb по сбору отзывов на произведения.

## Описание
Проект по сбору отзывов на произведения (фильмы, книги, музыка) 

Предусмотрена возможность добавления новых произведений, отзывов
к ранее добавленным, система рейтингов. 

Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий может быть расширен.
Произведению может быть присвоен жанр из списка предустановленных.
Новые жанры может создавать только администратор.

Сами произведения в YaMDb не хранятся.

Зарегистрированные пользователи оставляют к произведениям текстовые отзывы
и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). 
По оценкам автоматически высчитывается средняя оценка произведения.

Полная документация к API:  http://127.0.0.1:8000/redoc

## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/sarvilin/api_yamdb.git
```
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Участники:

[Сарвилин Алексей.](https://github.com/sarvilin/api_yamdb) 
- Категории, жанры, произведения и рейтинги: модели, view и эндпойнты для них.
- Докеризация, разработка процесса CI (непрерывной интеграции) с использованием GitHub Actions. 
- Подготовка  к production и deploy на YandexCloud.

[Панасенков Денис.](https://github.com/uchastnik/api_yamdb)
Управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail.

[Анучин Антон.](https://github.com/Homer-Ford/yamdb_final)
Отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов.

Проект создан в рамках обучения Яндекс Практикум.
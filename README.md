# api_yamdb

Данный проект создан в рамках обучения Яндекс Практикум:
```
Авторы:
Денис Панасенков
Сарвилин Алексей
Анучин Антон
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/uchastnik/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
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

Для заполнения базы данных из файлов csv
```
python manage.py ProcessCsv
```
# API для проекта YAMDB.

### Чтобы запустить проект нужно:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:vir2ozz2009/api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

Для Mac:
```
python3 -m venv venv
```

Для Windows:
```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в дирректирию с файлом manage.py:

```
cd api_yamdb
```

Выполнить миграции:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Регистрация пользователя:

Для начала надо зарегистрироваться, для этого нужно сделать POST-запрос к
ендпоинту http://127.0.0.1:8000/api/v1/auth/signup/ с параметрами:
{
"email": "user@example.com",
"username": "string"
}

Теперь требуется получить токен. Сделать это можно отправив POST-запрос к
ендпоинту http://127.0.0.1:8000/api/v1/auth/token/ с параметрами:
{
"username": "string",
"confirmation_code": "string"
}

### Теперь можно делать запросы к API проекта yatube:

Для получения всех произведений отправьте GET-запрос к ендпоинту
http://127.0.0.1:8000/api/v1/titles/

Для получения конкретного произведения отправьте GET-запрос
к ендпоинту http://127.0.0.1:8000/api/v1/titles/{titles_id}/

Более подробная информация содерится по адресу http://127.0.0.1:8000/redoc/
при запущенном сервере

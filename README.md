
## Описание
# Employee-birthdays сервис-подсказка: поздравь коллегу!

“Пользователи могут подписываться на других пользователей, добавлять их в список «Избранное», а также получать напоминания на почту.”

## Стек технологий

- Python
- Django
- Djangorestframework
- Djoser
- Gunicorn
- Docker
- Celery
- Redis
- PostgreSQL
- Sqlite
- drf-yasg

К проекту в контейнере возможно подключить базу данных PostgreSQL.
В режиме разработки (DEBUG = True) доступна динамическая документация по API.
Статическая документация находится в папке docs.

Динамическая документация: 

Локальный запуск:
http://localhost:8000/redoc/ и http://localhost:8000/swagger/

Запуск в контейнере:
http://localhost/redoc/ и http://localhost/swagger/

## Локальный запуск проекта

1. #### Склонируйте репозиторий:
```
git clone git@github.com:aleksei-astapoff/Employee-birthdays.git
```

2. #### Создайте и активируйте виртуальное окружение:
Команда для установки виртуального окружения на Mac или Linux:
```
python3 -m venv env
source env/bin/activate
```

Команда для установки виртуального окружения на Windows:
```
python -m venv venv
source venv/Scripts/activate
```

3. #### Выполните миграции:
```
python manage.py migrate
```

6. #### При необходимости создайте суперпользователя:
```
python manage.py createsuperuser
```
  #### Можно выполнить загрузку суперпользователя перед этим, создав файл .env и заполнив его по примеру env.example:
```
python manage.py birthdays_user
```

7. #### Запустите локальный сервер:
```
python manage.py runserver
```

8. #### Запустите в отдельном терминале Redis (он должен быть установлен в системе) и не закрывайте терминал:
```
redis-server
```
Проверьте ответ сервиса в новом терминале, введя команды последовательно:
```
redis-cli

PING
```
Ответ должен быть: PONG

Выйдите из Redis командой Ctrl + D.

9. #### В этом же терминале выполните запуск Celery:
Проверьте настройки в файле .env (# Настройка CELERY) — они должны соответствовать локальному запуску.
```
celery -A employee_birthdays worker --loglevel=info
```

10. #### Откройте новый терминал и выполните команду:
```
celery -A employee_birthdays beat --loglevel=info

```

Приложение будет доступно по адресу: http://localhost:8000/

В режиме разработчика будет доступна подсказка с доступными эндпоинтами.

## Локальный запуск проекта через Docker

1. #### Установите Docker согласно [инструкции](https://docs.docker.com/engine/install/ubuntu/)
Пользователям Windows нужно будет подготовить систему, установить для неё ядро Linux и после этого установить Docker.

2. #### В корневой директории проекта в терминале выполните команды:
Перед выполнением обязательно заполните файл .env по примеру env.example для запуска в контейнере!
База данных для запуска в контейнере PostgreSQL!
```
cd infra

docker-compose up --build

```

3. #### Примените миграции для создания таблиц баз данных.
Откройте новый терминал и перейдите в папку infra:
```
docker compose exec backend python manage.py migrate 
```

#### Возможно также создать суперпользователя, если заполнили файл .env
```
docker compose exec backend python manage.py createsuperuser
```

Приложение будет доступно по адресу: http://localhost:8000/

В режиме разработчика будет доступна подсказка с доступными эндпоинтами.

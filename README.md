## Статус workflow

![yamdb_workflow.yml](https://github.com/MaksimIgnatov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

# Yatube API

REST API-сервис для платформы ведения блогов.
Ссылка на развернутый проект:
```
http://158.160.96.125:8000/
```


## Переменные окружения:
Создаем файл example.env в дирректории infra:
```bash
touch ./infra/example.env
```
Шаблон наполнения:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
## Как запустить проект:
Клонировать репозиторий и перейти в папку infra в командной строке:
```bash
 git clone git@github.com:MaksimIgnatov/api_yamdb.git
```
```bash
 cd infra_sp2/infra
```
Запустите docker-compose:
```
docker-compose up -d
```
Выполните миграции:
```
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Соберите статистику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Проект доступен по адресу:
```
http://localhost/
```
## Заполнение базы данными:
Загружаем фикстуры:
```
docker-compose exec web python manage.py loaddata dump.json
```
## Примеры запросов

#### Документация к API

```http
  GET http://127.0.0.1:8000/redoc/
```

#### Получение публикаций

```http
  GET /api/v1/posts/
```
##### Response
```json
{
    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
    "results": [{...}]
}
```
#### Создание публикации
```http
  POST /api/v1/posts/
```
##### Request

```json
{
    "text": "string",
    "image": "string",
    "group": 0  
}
```
##### Response
```json
{
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": "2019-08-24T14:15:22Z",
    "image": "string",
    "group": 0
}
```

#### Получить JWT-токен

```http
  POST /api/jwt/create/
```
##### Request

```json
{
    "username": "string",
    "password": "string"
}
```
##### Response
```json
{
    "refresh": "string",
    "access": "string"
}
```
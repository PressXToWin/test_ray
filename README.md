# test_ray

Тестовое задание на позицию бэкенд-разработчика в компанию [Reactive Phone](ray.app).

Стек: Python 3.11, Django 4.2.7, PostgreSQL, Celery, Redis, NGINX.

Приложение позволяет создавать текстовые записи, а также получать их в автоматическом режиме с внешнего API [newsapi.org](newsapi.org). Для выполнения отложенных задач используется Celery, в качестве брокера очередей и для кэширования используется Redis. На проде лучше использовать два отдельных инстанса Redis, но для тестовых целей хватит и одного.

При установках по умолчанию раз в сутки в полночь происходит запрос к newsapi, который отдаёт все новости на русском языке за прошедший день, в которых упоминается требуемое слово (для тестовых целей в качестве примера взят "bitcoin").

Данные записи могут редактироваться пользователем, создавшим запись, либо суперпользователем. 

## Развертывание проекта
 - Склонируйте репозиторий. 
```
git clone https://github.com/PressXToWin/test_ray.git
```
 - Создайте .env файл в директории infra/, в котором должны содержаться следующие переменные для запуска:
```
NEWSAPI_KEY = '0d57b5f26dac4a54b8e09dc769ab7d94'

DB_NAME=ray
POSTGRES_USER=ray
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432

SECRET_KEY=django-insecure-v3r@g7e2-v6fn@!%_!fkrz3v_1bbwv7n*me7z2@^uwqpn^+0+
DEBUG=True
ALLOWED_HOSTS=127.0.0.1 yourdomain.com
CSRF_TRUSTED_ORIGINS=http://127.0.0.1 https://yourdomain.com
```

 - Создайте и запустите контейнеры Docker, выполнив команду:
```
docker compose up --build -d
```
 - После успешной сборки нужно создать суперпользователя:
```
docker compose exec backend python manage.py createsuperuser
```

## Эндпоинты API

```/api/posts/``` - принимает GET и POST-запросы. При GET-запросе отдаёт полный список постов, при POST-запросе создаёт новый пост. POST-запрос принимается только от аутентифицированного пользователя и отправляется в следующем формате:

```json
{
  "text": "текст поста"
}
```

```/api/posts/1/``` - GET-запрос возвращает пост с соответствующим номером. PUT- и PATCH-запросы от автора поста либо суперюзера редактируют пост, DELETE-запрос от автора поста либо суперюзера удаляет пост.

```/api/jwt/create``` - Возвращает JWT-токен, запрос должен быть отправлен в формате
```json
{
    "username": "user",
    "password": "pass"
}
```

## Запуск тестов

Код покрыт тестами, которые можно запустить, введя команду
```
docker compose exec backend python manage.py test
```
# Сайт Foodgram в контейнерах и CI/CD с помощью GitHub Actions
### Описание
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### Технологии
Django==3.2 | djangorestframework==3.12.4 | python-dotenv==1.0.0 | djoser==2.2.0 | pillow==10.0.0 | gunicorn==20.0.4

http://sweet-dish.hopto.org | admin@ya.ru | 1234

## Локальный запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/esaviv/foodgram-project-react.git
```
```
cd foodgram-project-react/infra/
```
Создать файл .env и заполнить его по образцу .env.template.

Перейдите в директорию, где лежит файл docker-compose.yml и запустит все контейнеры, описанные в конфиге:
```
docker compose up -d
```
Выполнить миграции:
```
docker compose exec backend python manage.py migrate
```
Собрать статику бэкенд-приложения:
```
docker compose exec backend python manage.py collectstatic --no-input
```
Загрузить в базу данных ингридиенты:
```
docker compose exec backend python manage.py import_csv
```
Создать супер пользователя, указав почту:
```
docker compose exec backend python manage.py createsuperuser
```
Открыть в браузере страницу http://localhost - проверить корректность работы проекта.

Перейти по адресу http://localhost/admin/ - убедиться, что страница отображается корректно.

Документация доступна по адресу:
```
http://localhost/api/docs/redoc.html
```

### Автор
esaviv

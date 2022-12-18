![Foodgram_workflow](https://github.com/desm80/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Мой стек технологий
img src="https://img.shields.io/badge/Python-7FFFD4?style=for-the-badge&logo=python&logoColor=black"/ img src="https://img.shields.io/badge/Django-7FFFD4?style=for-the-badge&logo=django&logoColor=black"/ img src="https://img.shields.io/badge/DjangoRESTFramework-7FFFD4/ img src="https://img.shields.io/badge/PostgreSQL-7FFFD4?style=for-the-badge&logo=posgresql&logoColor=black"/  img src="https://img.shields.io/badge/NGINX-7FFFD4?style=for-the-badge&logo=posgresql&logoColor=black"/ img src="https://img.shields.io/badge/gunicorn-7FFFD4?style=for-the-badge&logo=gunicorn&logoColor=black"/ img src="https://img.shields.io/badge/Docker-7FFFD4?style=for-the-badge&logo=docker&logoColor=black"/

# Продуктовый помощник - foodgram

Приложение, в котором пользователи могут публиковать рецепты, подписываться 
на публикации других пользователей, добавлять понравившиеся рецепты в список 
«Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд. В 
приложении реализована возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов.
Проект доступен по адресу http://178.154.201.53/ http://178.154.201.53/admin/

### Тестовые пользователи:
* Логин: admin (суперюзер)
* Email: admin@admin.net
* Пароль: admin


* Логин: user1
* Email: user1@user1.net
* Пароль: user1gfhjkm


* Логин: user2
* Email: user2@user2.net
* Пароль: user2gfhjkm


## Запуск проекта в Докер Контейнерах:

### Склонировать репозиторий на ВМ:

```git clone https://github.com/desm80/foodgram-project-react.git```

```cd foodgram-project-react```

### В папке infra заполните .env файл по приложенному образцу, убедитесь, что на вашей ВМ установлены Docker и Docker-compose

### Создайте и загрузите на свой аккаунт Docker Hub образы приложений проекта. В папках frontend и backend имеются соответствующие Dockerfile 

### Отредактируйте в файле docker-compose.yml названия имидж файлов на собственные

### В файле nginx.conf укажите адрес или имя своего сервера 

### В папке infra выполните команды:

```docker-compose up -d```

```docker-compose exec backend python manage.py collectstatic --no-input```

```docker-compose exec backend python manage.py migrate```

```docker-compose exec backend python manage.py createsuperuser```

```docker-compose exec backend python manage.py load_ingredients```


Проект запустится на адресе http://<Ваш адрес сервера>, увидеть спецификацию 
API вы сможете 
по адресу http://<Ваш адрес сервера>/api/docs/

Для проекта настроена процедура CI/CD через Git Hub actions. Для получения 
доступа к этой возможности заполните необходимые секреты в своем репозитории:

* ```DOCKER_USERNAME``` - имя пользователя в DockerHub
* ```DOCKER_PASSWORD``` - пароль пользователя в DockerHub
* ```HOST``` - адрес сервера
* ```USER``` - пользователь
* ```SSH_KEY``` - приватный ssh ключ
* ```PASSPHRASE``` - кодовая фраза для ssh-ключа
* ```DB_ENGINE``` - django.db.backends.postgresql
* ```DB_NAME``` - postgres (по умолчанию)
* ```POSTGRES_USER``` - postgres (по умолчанию)
* ```POSTGRES_PASSWORD``` - postgres (по умолчанию)
* ```DB_HOST``` - db
* ```DB_PORT``` - 5432
* ```SECRET_KEY``` - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
* ```TELEGRAM_TO``` - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* ```TELEGRAM_TOKEN``` - токен бота (получить токен можно у @BotFather, /token, имя бота)

foodgram_workflow запускается после команды git push в ветку main вашего 
репозитория.

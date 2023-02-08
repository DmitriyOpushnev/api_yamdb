# Final HomeWork Sprint №10
## API for YaMDB
### Описание
**Командный проект. API для сервиса отзывов YaMDB**
### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
### Установка
**Как запустить проект:**
```
Клонировать репозиторий и перейти в него в командной строке:
git clone https://github.com/DmitriyOpushnev/api_yamdb
cd api_yamdb
```
```
Cоздать и активировать виртуальное окружение:
python -m venv venv (если вы пользователь MacOS python3 -m venv venv)
source venv/bin/activate
```
```
Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip (если вы пользователь MacOS python3 -m pip install --upgrade pip)
pip install -r requirements.txt (если вы пользователь MacOS python3 pip install -r requirements.txt)
```
```
Выполнить миграции:
python manage.py migrate (если вы пользователь MacOS python3 manage.py migrate)
```
```
Запустить проект:
python manage.py runserver (если вы пользователь MacOS python3 manage.py runserver)
```
**Импорт csv файлов:**
```
python manage.py fill_db_from_csv
```

**Базовые эндопоинты API:**
```
"auth": "http://127.0.0.1:8000/api/v1/auth/",
"categories": "http://127.0.0.1:8000/api/v1/categories/",
"genres": "http://127.0.0.1:8000/api/v1/genres/",
"genres": "http://127.0.0.1:8000/api/v1/genres/",
"titles": "http://127.0.0.1:8000/api/v1/titles/",
"reviews": "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/",
"comments": "http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/",
```

**Все эндопоинты API:**
```
Все эндпоинты, а так же их параметры доступны по адресу: 
http://127.0.0.1:8000/redoc/
```

### Примеры запросов к API:
```
POST api/v1/categories/
http://127.0.0.1:8000/api/v1/categories/

Payload
{
  "name": "string",
  "slug": "string"
}

Response sample
201
{
  "name": "string",
  "slug": "string"
}

Response sample
400
{
  "field_name": [
    "string"
  ]
}
```
```
POST api/v1/auth/signup/
http://127.0.0.1:8000/api/v1/auth/signup/


Payload
{
  "email": "user@example.com",
  "username": "string"
}

Response sample
200
{
  "email": "string",
  "username": "string"
}

Response sample
400
{
  "field_name": [
    "string"
  ]
}

```
```
PATCH api/v1/users/{username}/
http://127.0.0.1:8000/api/v1/users/{username}/

Payload
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}

Response sample
200
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}

Response sample
400
{
  "field_name": [
    "string"
  ]
}
```
##### Авторы:
Авторизация и аутентификация, права доступа, пользователи - Дмитрий Опушнев.
https://github.com/DmitriyOpushnev/

Модели, view для произведений, категорий, жанров, импорт данных из csv файлов - Руслан Атаров.
https://github.com/ratarov

Модели, view для отзывов, комментариев, рейтингов - Андрей Кирилов.
https://github.com/Oktut

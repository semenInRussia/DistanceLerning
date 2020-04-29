# DistanceLerning (Дист. обучение)
Этот проект сделан для школ, для их учеников и их учителей.
## Вот пример испоьзования.
Директор создает школу. Сообщает учителям. Учителя ренистрируются создают классы приглашают учеников и спокойно могут сообщать им ДЗ.

## Установка
```
git clone https://github.com/semenInRussia/DistanceLerning.git
```
## Быстрый старт сервера
Windows
```
cd DistanceLerning
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```
Linux and Mac
```
cd DistanceLerning
pip3 -r install requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 8000
```

## Вот наш стек:
* Django 3.0 для web
* Django rest_framework для API


## Настройка базы данных:

Windows
```
python manage.py makemigrations
python manage.py migrate
```
Linux and Mac
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Создание сервера

Windows
```
python manage.py runserver
```
Linux and Mac
```
python3 manage.py runserver
```

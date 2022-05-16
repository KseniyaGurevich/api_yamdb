Клонировать репозиторий git clone git@github.com:KseniyaGurevich/api_yamdb.git

cd api_yamdb

Cоздать и активировать виртуальное окружение: python -m venv venv

source venv/scripts/activate

python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt: pip install -r requirements.txt

Выполнить миграции: python manage.py migrate

Запустить проект: python manage.py runserver

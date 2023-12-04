# АСВТ 2023. Курсовой проект. Система видеонаблюдения за АТМ

## Серверная часть

В данном репозитории приведен код сервреной части разрабатываемого ПО. Она отвечает за:

* Прием видеопотока и его анализ
* Сохранение контента
* Реализацию API, которое нужно для доступа к сохраненным видео, просмотра видео в режиме настоящего времени, управления
  системой

### ПО камеры

ПО камеры можно найти в следующем [репозитории](https://github.com/petiayko/ATM-CCTV-camera-soft)

### Лицензия

MIT

## Установка и запуск (первый способ)

1. Склонировать репозиторий:

``` bash
git clone https://github.com/petiayko/ATM-CCTV-server.git
```

2. Создать и активировать виртуальное окружение:

``` bash
cd ATM-CCTV-server
python -m venv venv
source venv/bin/active
```

3. Установить зависимости:

``` bash
pip install -r requirements.txt
```

4. Подготовиться к запуску:

``` bash
mkdir -p /data/config/cctv_manager
touch .env
echo APP_KEY='secret-key' > .env
cd cctv_manager
python manage.py migrate
python manage.py loaddata fixtures/users.json
```

5. Запустить сервер:

``` bash
python manage.py runserver 0.0.0.0:8000
```

Пункты 4-5 можно заменить на

``` bash
chmod +x entrypoint.sh
./entrypoint.sh
```

## Установка и запуск (второй способ)

1. Склонировать репозиторий:

``` bash
git clone https://github.com/petiayko/ATM-CCTV-server.git
```

2. Запустить docker-compose:

``` bash
cd ATM-CCTV-server
docker-compose up 
```

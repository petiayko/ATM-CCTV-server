#!/bin/sh

export IS_DOCKER_COMPOSE=1
cd cctv_manager
python manage.py migrate
python manage.py loaddata fixtures/users.json
printf "\n\n\t\tsuperuser created:\n\t\t\tlogin - admin\n\t\t\tpassword - 8Xgex7E6CRCF4wz\n\n\n"
python manage.py runserver 0.0.0.0:8000

exec $cmd

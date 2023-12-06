#!/bin/sh

export IS_DOCKER_COMPOSE=1
mkdir -p /data/config/cctv_manager
cd cctv_manager

echo "Apply database migrations"
python manage.py migrate
echo "Load fixtures"
python manage.py loaddata fixtures/groups.json
python manage.py loaddata fixtures/users.json
printf "\n\n\t\tnetwork administrator created:\n\t\t\tlogin - admin\n\t\t\tpassword - 8Xgex7E6CRCF4wz\n\n\n"
echo "Starting server"
python manage.py runserver 0.0.0.0:8000

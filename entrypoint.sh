#!/bin/sh

echo "Aguardando banco..."

sleep 10

python manage.py migrate

python manage.py collectstatic --noinput

exec "$@"
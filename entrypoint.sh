#!/usr/bin/env bash
set -e

PRIVATE_JWT_KEY_PATH="jwt_auth/keys/jwt_private.pem"
PUBLIC_JWT_KEY_PATH="jwt_auth/keys/jwt_public.pem"

if [ ! -f "$PRIVATE_JWT_KEY_PATH" ]; then
    openssl genpkey -algorithm RSA -out "$PRIVATE_JWT_KEY_PATH" -pkeyopt rsa_keygen_bits:2048
fi

if [ ! -f "$PUBLIC_JWT_KEY_PATH" ]; then
    openssl rsa -pubout -in "$PRIVATE_JWT_KEY_PATH" -out "$PUBLIC_JWT_KEY_PATH"
fi

python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py makemigrations citra_account --noinput
python3 manage.py makemigrations lobby --noinput
python3 manage.py migrate --noinput
exec gunicorn --bind 0.0.0.0:$INTERNAL_PORT core.wsgi:application

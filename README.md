# citra-backend-v2
An unofficial Django-based backend for Citra web API

## Simple Usage
### Directly

Setup:
```sh
pip install -r requirements.txt
export ALLOWED_HOSTS=localhost
export INTERNAL_PORT=5000
export DEBUG=true
bash entrypoint.sh
```

Test query all rooms:
```sh
> curl http://localhost:5000/lobby
{"rooms": []}
```

### Docker

Setup:
```sh
docker build -t citra-backend-v2 .
docker run --rm -it \
  -p 5000:5000 \
  -e ALLOWED_HOSTS=0.0.0.0 \
  -e INTERNAL_PORT=5000 \
  -e DEBUG=true \
  -v "$(pwd)/jwt_auth/keys:/app/jwt_auth/keys" \
  citra-backend-v2
```

## Environment Variables

| Variable               | Default                              | Description                                                                       |
| ---------------------- | ------------------------------------ | --------------------------------------------------------------------------------- |
| `SECRET_KEY`           | insecure development key in settings | Django secret key. Set this explicitly in production.                             |
| `DEBUG`                | `false`                              | Enables debug mode. When `true`, SQLite is used indead of PostgreSQL.             |
| `INTERNAL_PORT`        | `""`                                 | Internal port used for the app                                                    |
| `ALLOWED_HOSTS`        | `""`                                 | Comma-separated list of allowed hosts, for example `example.com,www.example.com`. |
| `POSTGRES_DB`          | `""`                                 | PostgreSQL database name.                                                         |
| `POSTGRES_USER`        | `""`                                 | PostgreSQL username.                                                              |
| `POSTGRES_PASSWORD`    | `""`                                 | PostgreSQL password.                                                              |
| `EMAIL_HOST`           | `""`                                 | SMTP host.                                                                        |
| `EMAIL_ADDRESS`        | `""`                                 | SMTP username and default sender address.                                         |
| `EMAIL_PASSWORD`       | `""`                                 | SMTP password.                                                                    |
| `DJANGO_LOG_FORMATTER` | `verbose`                            | Logging formatter for console output.                                             |
| `DJANGO_LOG_LEVEL`     | `INFO`                               | Log level for Django logs.                                                        |
| `LOBBY_LOG_LEVEL`      | `INFO`                               | Log level for the `lobby` app.                                                    |


# citra-backend-v2

An unofficial Django-based backend for Citra 3DS emulator web API

### Features

- Registration and querying of lobbies at `/lobby`
- Account registration and management at `/` (Should only be used with `HTTPS`)
  - Setting avatars
  - Citra token generation (Associates users with accounts)

## Usage
### Simple Backend Setup with Debug
#### Direct

```sh
pip install -r requirements.txt
export ALLOWED_HOSTS=localhost
export INTERNAL_PORT=5000
export DEBUG=true
bash entrypoint.sh
```

#### Docker

```sh
docker build -t citra-backend-v2 .
docker run --rm -it \
  -p 5000:5000 \
  -e ALLOWED_HOSTS=localhost \
  -e INTERNAL_PORT=5000 \
  -e DEBUG=true \
  -v "$(pwd)/jwt_auth/keys:/app/jwt_auth/keys" \
  citra-backend-v2
```

### Citra Configurations

####  Citra Client

Set URL in `qt-config.ini`:
```ini
web_api_url\default=false
web_api_url=http://localhost:5000
```

#### Configure `citra-room`

Pass URL as argument:
```sh
--web-api-url "http://localhost:5000"
```

### Testing
#### Query All Rooms with `curl`

```sh
> curl http://localhost:5000/lobby
{"rooms": []}
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
| `EMAIL_ADDRESS`        | `""`                                 | Email address used for sending mails for account recovery requests.               |
| `EMAIL_PASSWORD`       | `""`                                 | Email account password.                                                           |
| `EMAIL_HOST`           | `""`                                 | Host URL of email account.                                                        |
| `DJANGO_LOG_FORMATTER` | `verbose`                            | Logging formatter for console output.                                             |
| `DJANGO_LOG_LEVEL`     | `INFO`                               | Log level for Django logs.                                                        |
| `LOBBY_LOG_LEVEL`      | `INFO`                               | Log level for the `lobby` app.                                                    |

Extended Django configurations can be done in `core/settings.py`

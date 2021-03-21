## cornershop-backend-test

### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000

### Cargue data inicial
* `./manage.py loaddata fixtures.json`
* `./manage.py loaddata fixtures_menu.json`
### Login
* Para loguearte a la plataforma debes usar username=nora y password=cornershoptest
### Slack bot
Debe tener una app en un Workspace en Slack y un bot con los permisos:
* chat:write
* users:read
* users:read.email
* incoming-webhook

Además debe generar un archivo `.env` en el directorio raíz del proyecto con la siguientes variable obligatoria que corresponde a  OAuth Tokens del bot.

```
BOT_USER_ACCESS_TOKEN=xxxxxx-xxxxxx-xxxxxxx
```
### Celery
Para este proyecto se seteó la hora de envió del recordatorio todos los días a las 8:30 am hora de santiago de chile

```
CELERYBEAT_SCHEDULE = {
    'daily-reminder-menu': {
        'task': 'slack_bot.tasks.send_message_to_users',
        'schedule': crontab(minute=30,hour=8)
    },
```
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

### Load initial data
* `./manage.py loaddata fixtures.json`
* `./manage.py loaddata fixtures_menu.json`
### Login
* To login to the platform you must use username=nora and password=cornershoptest
### Slack bot
You must have an app in a Workspace in Slack and a bot with the permissions:
* chat:write
* users:read
* users:read.email
* incoming-webhook

In addition, you must generate a `.env` file in the backend_test directory of the project with the following obligatory variable that corresponds to the bot's OAuth Tokens.

```
BOT_USER_ACCESS_TOKEN=xxxxxx-xxxxxx-xxxxxxx
```
### Celery

For this project, the time to send the reminder was set every day at 8:30 am Santiago de Chile time
```
CELERYBEAT_SCHEDULE = {
    'daily-reminder-menu': {
        'task': 'slack_bot.tasks.send_message_to_users',
        'schedule': crontab(minute=30,hour=8)
    },
```

To run celery
```
celery -A backend_test worker --beat --scheduler django --loglevel=info
```

You must create a Menu for today, for that you must first log in and create lunch options and then create a Menu.

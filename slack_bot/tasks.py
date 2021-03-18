from celery.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import  shared_task
from datetime import datetime, timedelta
from backend_test.celery import app
from django.utils import timezone
from slack_bot.utils import send_message_to_users
from django.contrib.sites.models import Site

from menu_manager.models import (
   Menu,
   EmployeesMenuAnswer,
)

logger = get_task_logger(__name__)



@app.task
def try_celery():
    logger.info("Trying out Celery")
    print("jajajaja")

@shared_task
def test_add(x, y):
    print ('Ejecución finalizada')
    return x + y

@app.task
def send_message():
    logger.info('Mensaje Enviado')
    current_site = Site.objects.get_current()
    # Get today's Menu
    today = timezone.now()
    today_menu = Menu.objects.filter(start_date=today.date()).first()
    answer = EmployeesMenuAnswer.objects.filter(menu=today_menu).first()
    # Construct url's menu if there is a menu today
    if today_menu:
        url = f'https://{current_site.domain}/menu/{answer.pk}'
        message = ":wave:, Hola  en este link podrás encontrar el menu de hoy " + url
        send_message_to_users(message)
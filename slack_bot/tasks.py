from celery.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import  shared_task
from datetime import datetime, timedelta
from backend_test.celery import app
from django.utils import timezone
from slack_bot.utils import  save_users_info, send_message_to_user
from django.contrib.sites.models import Site

from menu_manager.models import (
   Menu,
   Answer,
   Employee

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
def send_message_to_users():
    current_site = Site.objects.get_current()
    # Get today's Menu
    today = timezone.localtime(timezone.now())
    today_menu = Menu.objects.filter(start_date=today.date()).first() # usar get

    if today_menu:
        save_users_info(today_menu)
        employees = Employee.objects.all()

    # Construct url's menu if there is a menu today
        for employee in employees:
            # Send message to active users
            if employee.is_active:
                answer = Answer.objects.filter(menu=today_menu,employee=employee).first()
                url = f'https://{current_site.domain}/menu/{answer.pk}'
                message = ":wave:, Hola  en este link podrás encontrar el menu de hoy " + url
                send_message_to_user(message,employee.user_id)
            # desactivate user
            employee.is_active=False
            employee.save()
        # Set menu state
        today_menu.is_sent=True
        today_menu.save()
        logger.info('Mensaje Enviado')
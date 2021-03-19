import logging
import os
import datetime
import requests
import slack

from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from dateutil.relativedelta import relativedelta

from menu_manager.models import (
    Menu,
    Options,
    Answer,
    Employee
)


client  = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)

def get_list_of_users():
    # TODO : PAGINATION
    users = client.api_call("users.list")
    if users.get('ok'):
        return users['members']


def save_users_info(today_menu):
    users = get_list_of_users()

    if users:
        for user in users:
            if 'email' in user['profile']:
                employee, created = Employee.objects.update_or_create(user_id=user['id'],
                                        name=user['profile']['real_name'],
                                        email=user['profile']['email'],
                                        is_active=True,
                                        )
                Answer.objects.create(menu=today_menu,employee=employee)



def send_message_to_user(response_msg,user_id):
    try:
        client.chat_postMessage(
                        channel=user_id,
                        text=response_msg
                    )
    except ValueError as e:
        print(" error en "+ str(type(e))


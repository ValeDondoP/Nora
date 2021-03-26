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
    Answer,
    Employee
)


client  = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)

def get_list_of_users():
    """Requests list of member of a slack workspace """

    users = client.api_call("users.list")
    if users.get('ok'):
        return users['members']
    raise Exception()

def save_users_info(today_menu):
    """ Save users data in Employee and set is_active if there are part of user list in slack """

    users = get_list_of_users()

    if users:
        for user in users:
            if 'email' in user['profile']:
                employee, created = Employee.objects.update_or_create(
                                        user_id=user['id'],
                                        name=user['profile']['real_name'],
                                        email=user['profile']['email'],
                )
                # active unactive employee to send message
                if employee:
                    employee.is_active=True
                    employee.save()

                # create or get the answer for the employee
                Answer.objects.get_or_create(menu=today_menu,employee=employee)

def send_message_to_user(response_msg,user_id):
    """ send message to a specific user and message in slack """
    try:
        client.chat_postMessage(
                        channel=user_id,
                        text=response_msg
                    )
    except:
        raise Exception()




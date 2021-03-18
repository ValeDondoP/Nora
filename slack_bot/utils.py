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


client  = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)

def get_list_of_users():
    users = client.api_call("users.list")
    if users.get('ok'):
        return users['members']

def send_message_to_users(response_msg):
    users = get_list_of_users()
    if users:
        for user in users:
            if user['is_bot'] == False:
                client.chat_postMessage(
                    channel=user['id'],
                    text=response_msg
                )

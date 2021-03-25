import json
from unittest import mock

from unittest.mock import patch, Mock
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from slack_bot.utils import get_list_of_users, save_users_info, send_message_to_user
from slack_bot.tasks import send_message_to_users
from django.contrib.sites.models import Site
from menu_manager.models import (
    Menu,
    Employee,
    Option,
    Answer
)

class TestUtils(TestCase):

    def test_save_users_info(self):
        """ Test function save_users_info """
        today = timezone.now()
        today_menu = Menu.objects.create(start_date=today)

        save_users_info(today_menu)

        self.assertIsNotNone(Employee.objects.first())
        number_of_employees = Employee.objects.all().count()
        # if I call the function again it should not change the number of employees in datatabase
        save_users_info(today_menu)
        self.assertEquals(number_of_employees,Employee.objects.all().count())
"""
class TestTask(TestCase):
    fixtures = ['fixtures.json','fixtures_menu.json']
    def setUp(self):
        current_site = Site.objects.get_current()
        today = timezone.now()
        today_menu = Menu.objects.create(start_date=today)
        today_menu.options.add(Option.objects.first())
        today_menu.save()
        answer= Answer.objects.first()
        self.today_menu =today_menu
        employee = Employee.objects.create(name='Valentina',email='vurzua@mail.com',user_id='111')
        answer.menu = today_menu
        answer.employee = employee
        answer.save()
        self.slack_api_response = [
            {
                "ok": True,
                "channel": "C1H9RESGL",
                "ts": "1503435956.000247",
                "message": {
                    "text": "Here's a message for you",
                    "username": "ecto1",
                    "bot_id": "B19LU7CSY",
                    "attachments": [
                        {
                            "text": "This is an attachment",
                            "id": 1,
                            "fallback": "This is an attachment's fallback"
                        }
                    ],
                    "type": "message",
                    "subtype": "bot_message",
                    "ts": "1503435956.000247"
                }
            }
        ]

    @patch("requests.get")
    def test_send_message_to_users(self, mock_post):
    
        mock_response = mock.Mock()
        # set the json response to what we're expecting
        mock_response.json.return_value = self.slack_api_response
         # Define response for the fake API
        mock_post.return_value = mock_response
        # Call the function
        send_message_to_users()
        print(self.today_menu.is_sent)

        assert True
        """
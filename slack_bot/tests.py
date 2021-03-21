from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from slack_bot.utils import get_list_of_users, save_users_info, send_message_to_user
from menu_manager.models import (
    Menu,
    Employee
)

class TestViews(TestCase):

    def test_save_users_info(self):
        today = timezone.now()
        today_menu = Menu.objects.create(start_date=today)

        save_users_info(today_menu)

        self.assertIsNotNone(Employee.objects.first())

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from slack_bot.utils import get_list_of_users, save_users_info, send_message_to_user
from menu_manager.models import (
    Menu,
    Employee
)

class TestUtils(TestCase):

    def test_save_users_info(self):
        """ Test function save_users_info """
        today = timezone.now()
        today_menu = Menu.objects.create(start_date=today)

        save_users_info(today_menu) # should not call the api, mock the api

        self.assertIsNotNone(Employee.objects.first())
        number_of_employees = Employee.objects.all().count()
        # if I call the function again it should not change the employees in datatabase
        save_users_info(today_menu)
        self.assertEquals(number_of_employees,Employee.objects.all().count())

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from slack_bot.utils import get_list_of_users, save_users_info, send_message_to_user
from slack_bot.tasks import send_message_to_users
from django.test.utils import override_settings
from django.conf import settings
from menu_manager.models import (
    Menu,
    Option,
    Employee,
    Answer
)

class TestUtilsAndTasks(TestCase):

    def setUp(self):
        today = timezone.now()
        today_menu = Menu.objects.create(start_date=today)
        option = Option.objects.create(meal='cazuela, ensalada y postre')
        today_menu.options.add(option)
        today_menu.save()
        self.today_menu = today_menu


    def test_save_users_info(self):
        """ Test function save_users_info """

        save_users_info(self.today_menu) # this call fake api

        self.assertIsNotNone(Employee.objects.first())
        self.assertIsNotNone(Answer.objects.first())

        number_of_employees = Employee.objects.all().count()

        # if I call the function again it should not change the employees in datatabase
        save_users_info(self.today_menu)
        self.assertEqual(number_of_employees,Employee.objects.all().count())

    def test_send_message_to_users(self):
        """ Test function send_message_to_users """

        send_message_to_users() # this call mocked api

        answer = Answer.objects.first()
        menu = Menu.objects.get(pk=self.today_menu.pk)

        # Check that today's menu  is sent
        self.assertTrue(menu.is_sent)
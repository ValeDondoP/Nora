import json
import datetime
from datetime import date
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from menu_manager.models import (
    Menu,
    Option,
    Answer,
    Employee
)


class TestViews(TestCase):
    fixtures = ['fixtures.json','fixtures_menu.json']

    def setUp(self):
        self.client = Client()
        self.menu_url =  reverse('menu_manager:create_menu')
        self.client.login(username="nora", password="cornershoptest")
        answer = Answer.objects.first()
        menu = Menu.objects.first()
        self.answer = answer
        self.menu = menu
        self.date = timezone.now().date() + timedelta(days=1)

    def test_menu_create_POST(self):
        """test to check if can create menu in MenuCreateView"""

        url = self.menu_url
        option = Option.objects.create(meal="arroz con pescado")
        response = self.client.post(url,{
            'start_date':self.date ,
            'options' : [option.pk],
        })
        menu = Menu.objects.get(options=option)
        self.assertEqual(Menu.objects.all().count(),2)
        self.assertEqual(menu.options.first(),option)
        self.assertEqual(menu.start_date,self.date)

    def test_menu_create_POST_without_options(self):
        """test to check if can create menu in MenuCreateView without options"""

        url = self.menu_url
        response = self.client.post(url,{
            'start_date': '2021-03-12',
            'options' : [],
        })
        self.assertEqual(response.status_code, 200)

    def test_menu_list_view(self):
        """ test to check  MenuListView object_list"""

        response = self.client.get(reverse('menu_manager:menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/menu_list.html')
        self.assertTrue(len(response.context['object_list']) == Menu.objects.all().count())

    def test_update_menu_view(self):
        """ test to check if can update menu in MenuUpdateView"""

        response = self.client.post(
            reverse('menu_manager:update_menu',
            args=[self.menu.pk]),
            { 'start_date': '2022-03-12',
              'options': [self.menu.options.first().pk]
        })
        # this menu is already sent
        self.assertEqual(response.status_code, 403)

    def test_delete_menu_view(self):
        """ test to check if can delete menu in MenuDeleteView"""

        response = self.client.get(reverse('menu_manager:delete_menu',args=[self.menu.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0,Menu.objects.all().count()) # there was one menu in database

    def test_option_create_view(self):
        """ test if can create option in OptionMenuCreateView """

        response = self.client.post(
            reverse('menu_manager:create_option'),
            { 'form-TOTAL_FORMS': 2,
              'form-INITIAL_FORMS': 0,
              'form-MAX_NUM_FORMS': 6,
              # First meal data
              'form-0-meal': 'pizza',

              # Second meal data
              'form-1-meal': 'sushi',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Option.objects.all().count(),4) # 2 initial options in fixtures_menu.json

    def test_today_menu_context(self):
        """ test to check is_active key in context_data  in TodayMenuView """

        response = self.client.get(reverse('menu_manager:today_menu',args=[self.answer.pk]))
        hour = timezone.localtime(timezone.now()).hour
        minutes = timezone.localtime(timezone.now()).minute
        if hour < 11 and hour >= 8:
            self.assertTrue(response.context['is_active'])
        elif hour==11 and minutes==0:
            self.assertTrue(response.context['is_active'])
        else:
            is_active = 'is_active' in response.context
            self.assertFalse(is_active)

    def test_answer_list_view_context(self):
        """ test to check menu key in context_data in AnswerListView """

        response = self.client.get(reverse('menu_manager:results',args=[self.menu.pk]))
        self.assertIsNotNone(response.context['menu'])

    def test_answer_list_get_queryset(self):
        """ test to check queryset in AnswerListView """

        response = self.client.get(reverse('menu_manager:results',args=[self.menu.pk]))
        self.assertQuerysetEqual(
            response.context['object_list'],
            Answer.objects.filter( menu=self.menu),
            transform= lambda x:x
        )


import json
import datetime
from datetime import date
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from menu_manager.views import *
from menu_manager.models import (
    Menu,
    Options,
    Answer,
    Employee
)


class TestViews(TestCase):
    fixtures = ['fixtures.json',"fixtures_menu.json"]


    def setUp(self):
        self.client = Client()
        self.menu_url =  reverse('menu_manager:create_menu')
        self.client.login(username="nora", password="cornershoptest")
        answer = Answer.objects.first()
        menu = Menu.objects.first()
        self.answer = answer
        self.menu = menu

    def test_menu_create_POST(self):
        """test to check if can create menu in MenuCreateView"""

        url = self.menu_url
        option = Options.objects.create(meal="arroz con pescado")
        response = self.client.post(url,{
            'start_date': '2021-03-12',
            'options' : [option.pk],
        })
        menu = Menu.objects.get(options=option)
        self.assertEquals(Menu.objects.all().count(),2)
        self.assertEquals(menu.options.first(),option)
        start_date = date.fromisoformat('2021-03-12')
        self.assertEquals(menu.start_date,start_date)

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
        start_date = date.fromisoformat('2022-03-12')
        menu = Menu.objects.get(start_date=start_date)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(menu.start_date,start_date)

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
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Options.objects.all().count(),4) # 2 initial options in fixtures_menu.json

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



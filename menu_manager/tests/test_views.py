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

    fixtures = ['fixtures.json', 'fixtures_menu.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='nora', password='cornershoptest')

        self.option =  Option.objects.first()
        self.past_menu = Menu.objects.first()
        self.date = timezone.now().date() + timedelta(days=1)

        # Create menu with future start_date to test valid update and delete form
        current_menu = Menu.objects.create(start_date=self.date)
        current_menu.options.add(self.option)
        current_menu.save()

        self.menu = current_menu
        self.answer =  Answer.objects.first()
        self.menu_url = reverse('menu_manager:create_menu')


    def test_menu_create_POST(self):
        """ Test to check if can create menu in MenuCreateView """

        url = self.menu_url
        option = Option.objects.create(meal='arroz con pescado')
        response = self.client.post(url, {'start_date': self.date
                                    + timedelta(days=1),
                                    'options': [option.pk]})

        # check menu created
        menu = Menu.objects.get(options=option)
        self.assertEqual(Menu.objects.all().count(), 3)
        self.assertEqual(menu.options.first(), option)
        self.assertEqual(menu.start_date, self.date + timedelta(days=1))

    def test_menu_create_POST_without_options(self):
        """ Test to check if can create menu in MenuCreateView without options """

        url = self.menu_url
        response = self.client.post(url, {'start_date': self.date + timedelta(days=2),
                                    'options': []})
        self.assertEqual(response.status_code, 200)

        # check that the menu was not created
        is_menu_created = Menu.objects.filter(start_date=self.date + timedelta(days=2)).exists()
        self.assertFalse(is_menu_created)

    def test_menu_create_POST_without_date(self):
        """ Test to check if can create menu in MenuCreateView without start_date """

        url = self.menu_url
        response = self.client.post(url,
                                    {'start_date': '',
                                    'options': self.option})

        # does not redirect to success url
        # TODO: que hacer en este cao
        self.assertEqual(response.status_code, 200)


    def test_menu_create_POST_with_menu_date_taken(self):
        """ Test to check if can create menu in MenuCreateView with a date already taken by other menu """

        url = self.menu_url
        response = self.client.post(url,
                                    {'start_date': self.past_menu.start_date,
                                    'options': [self.option.pk]})
        self.assertEqual(response.status_code, 200)

        # check if the menu was created
        number_of_menus = Menu.objects.filter(start_date=self.past_menu.start_date).count()
        self.assertEqual(number_of_menus,1)

    def test_menu_list_view(self):
        """ Test to check  MenuListView object_list """

        response = self.client.get(reverse('menu_manager:menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/menu_list.html')
        self.assertTrue(len(response.context['object_list'])
                        == Menu.objects.all().count())

    def test_update_menu_view_fails(self):
        """ Test to check if can not update menu in MenuUpdateView because the menu is sent """

        response = self.client.post(reverse('menu_manager:update_menu',
                                    args=[self.past_menu.pk]),
                                    {'start_date': self.date + timedelta(days=2), # update start_date
                                    'options': [self.menu.options.first().pk]})

        # this menu is already sent therefore it should return 403
        self.assertEqual(response.status_code, 403)

    def test_delete_menu_view(self):
        """ Test to check if can delete menu in MenuDeleteView """

        response = self.client.get(reverse('menu_manager:delete_menu',
                                   args=[self.menu.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, Menu.objects.all().count())  # there were 2 menus originally

    def test_delete_menu_view_with_sent_menu(self):
        """ Test to check if can delete menu in MenuDeleteView """

        response = self.client.get(reverse('menu_manager:delete_menu',
                                   args=[self.past_menu.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(2, Menu.objects.all().count()) # there are two menus in database and no one is deleted

    def test_option_create_view(self):
        """ Test if can create option in OptionMenuCreateView """

        response = self.client.post(reverse('menu_manager:create_option'
                                    ),
            {  # First meal data and second meal data
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-MAX_NUM_FORMS': 6,
            'form-0-meal': 'pizza',
            'form-1-meal': 'sushi',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/create_option/option_list')
        self.assertEqual(Option.objects.all().count(), 4)  # 2 initial options in fixtures_menu.json

    def test_invalid_option_create_view(self):
        """ Test if can create option in OptionMenuCreateView """

        response = self.client.post(reverse('menu_manager:create_option'
                                    ), {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-MAX_NUM_FORMS': 6,
            'form-0-meal': '',
            'form-1-meal': '',
            })

        self.assertEqual(Option.objects.all().count(), 2)

    def test_today_menu_context(self):
        """ Test to check is_active key in context_data  in TodayMenuView """

        # can see without login
        self.client.logout()
        response = self.client.get(reverse('menu_manager:today_menu',
                                   args=[self.answer.pk]))
        self.assertEqual(response.status_code,200)

        hour = timezone.localtime(timezone.now()).hour
        minutes = timezone.localtime(timezone.now()).minute
        if hour < 11 and hour >= 8:
            self.assertTrue(response.context['is_active'])
            self.assertContains(response,'¡Escoge tu almuerzo!')
        elif hour == 11 and minutes == 0:
            self.assertTrue(response.context['is_active'])
            self.assertContains(response,'¡Escoge tu almuerzo!')
        else:
            is_active = 'is_active' in response.context
            self.assertFalse(is_active)
            self.assertContains(response,'Lo siento! el menu expiró :( ')

    def test_answer_list_view_context(self):
        """ Test to check menu key in context_data in AnswerListView """

        response = self.client.get(reverse('menu_manager:results',
                                   args=[self.menu.pk]))
        self.assertIsNotNone(response.context['menu'])

    def test_answer_list_get_queryset(self):
        """ test to check queryset in AnswerListView """

        response = self.client.get(reverse('menu_manager:results',
                                   args=[self.menu.pk]))
        self.assertQuerysetEqual(response.context['object_list'],
                                 Answer.objects.filter(menu=self.menu),
                                 transform=lambda x: x)

    def test_answer_employee_list_view_with_valid_user(self):
        """ Tests to check if I login I can enter to see answer list for a specific menu """

        response = self.client.get(reverse('menu_manager:results',args=[self.menu.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'web/answer_list.html')

    def test_answer_employee_list_view_with_anonymous_user(self):
        """ Tests if anonymus o not registered user can see the answer list for a specific menu """

        # Log out
        self.client.logout()
        response = self.client.get(reverse('menu_manager:results',args=[self.menu.pk]))

        # redirect to login
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, f'/accounts/login/?next=/results/{self.menu.pk}')

        # try to login with diferent user
        self.client.login(username="vale", password="cornershoptest")
        response = self.client.get(reverse('menu_manager:results',args=[self.menu.pk]))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, f'/accounts/login/?next=/results/{self.menu.pk}')


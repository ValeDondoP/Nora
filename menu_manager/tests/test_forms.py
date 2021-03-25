from django.test import TestCase
from menu_manager.forms import MenuForm, AnswerForm, MenuFormUpdate
from menu_manager.models import Option, Answer, Menu, Employee
from django.utils import timezone
from datetime import datetime, timedelta

class TestForms(TestCase):

    fixtures = ['fixtures_menu.json']

    def setUp(self):
        option = Option.objects.first()
        answer = Answer.objects.first()
        self.option = option
        self.answer = answer
        self.date = timezone.now().date() + timedelta(days=1)

        # Create a menu with start_date in the future

        menu = Menu.objects.create(start_date=self.date)
        menu.options.add(self.option)
        menu.save()
        self.menu = menu

    def test_valid_menu_form(self):
        """ test to check if menu form is valid """

        data = {'start_date': self.date + timedelta(days=1),
                'options': [self.option.pk]}
        form = MenuForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_menu_form(self):
        """ test to check if menu form is invalid """

        # set a past date

        data = {'start_date': '1999-07-01', 'options': [self.option.pk]}

        form = MenuForm(data=data)
        self.assertFalse(form.is_valid())

        # set not options

        data.update({'options': []})
        form = MenuForm(data=data)
        self.assertFalse(form.is_valid())

        # create a menu with a start_date already used

        data.update({'start_date': self.date,
                    'options': [self.option.pk]})

        form = MenuForm(data=data)
        self.assertFalse(form.is_valid())

        # create a menu with a start_date as number

        data.update({'start_date': ''})
        form = MenuForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_menu_update_form(self):
        """ test to check if menu update form is valid """

        option = Option.objects.last()
        valid_data = {
            'start_date': self.menu.start_date,
            'options': [option.pk]
        }
        form = MenuFormUpdate(instance=self.menu, data=valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_menu_update_form(self):
        """ test to check if menu update form is invalid """

        invalid_data = {'start_date': '2020-03-04',
                        'options': [self.option.pk]}

        # try to update a menu with a past date

        form = MenuFormUpdate(instance=self.menu, data=invalid_data)
        self.assertFalse(form.is_valid())

        # try to update a menu with no options

        invalid_data.update({'options': []})
        form = MenuFormUpdate(instance=self.menu, data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_valid_answer_form(self):
        """ test to check if Answer form is valid """

        valid_data = {
            'menu': self.answer.menu.pk,
            'menu_option': self.answer.menu_option.pk,
            'comentaries': 'ensalada sin tomate'
        }
        form = AnswerForm(instance=self.answer, data=valid_data)
        self.assertTrue(form.is_valid())

        # Send answer without commentaries it is allowed

        valid_data.update({'comentaries': ''})
        form = AnswerForm(instance=self.answer, data=valid_data)
        self.assertTrue(form.is_valid())


    def test_invalid_answer_form(self):
        """ test to check if Answer form is invalid """
        # send form without menu_option
        form = AnswerForm(instance=self.answer,
                          data={'menu': self.answer.menu.pk,
                          'menu_option': '',
                          'comentaries': 'ensalada sin tomate'})

        self.assertFalse(form.is_valid())

        # send form without menu
        form = AnswerForm(instance=self.answer,
                          data={
                          'menu_option': self.answer.menu_option.pk,
                          'comentaries': 'ensalada sin tomate'})
        self.assertFalse(form.is_valid())

        #
        employee = self.answer.employee
        shammer_employee = Employee.objects.create(name='Impostor',email='impostor@mail.com')

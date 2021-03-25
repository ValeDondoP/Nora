from django.test import TestCase
from menu_manager.forms import MenuForm, AnswerForm, MenuFormUpdate
from menu_manager.models import Option, Answer, Menu
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
        menu =  Menu.objects.create(start_date=self.date)
        menu.options.add(self.option)
        menu.save()
        self.menu = menu

    def test_valid_menu_form(self):
        """ test to check if menu form is valid """

        form = MenuForm(data={'start_date':self.date + timedelta(days=1),
                              'options':[self.option.pk]})
        self.assertTrue(form.is_valid())

    def test_invalid_menu_form(self):
        """ test to check if menu form is invalid """

        # set a past date
        form = MenuForm(data={'start_date':'2020-07-03','options':[self.option.pk]})
        self.assertFalse(form.is_valid())

        # set not options
        form = MenuForm(data={'start_date': self.date + timedelta(days=1),'options':[]})
        self.assertFalse(form.is_valid())

        # create a menu with a start_date already used
        form = MenuForm(data={'start_date': self.date,'options':[self.option.pk]})
        self.assertFalse(form.is_valid())


    def test_valid_menu_update_form(self):
        """ test to check if menu form is invalid """

        form = MenuFormUpdate(instance=self.menu,data={'start_date':self.menu.start_date,
                              'options':[self.option.pk]})
        self.assertTrue(form.is_valid())

    def test_invalid_menu_update_form(self):
        """ test to check if menu update form is invalid """

        # try to update a menu with a past date
        form = MenuFormUpdate(instance=self.menu,data={'start_date': '2020-03-04',
                              'options':[self.option.pk]})
        self.assertFalse(form.is_valid())

        # try to update a menu with no options
        form = MenuFormUpdate(instance=self.menu,data={'start_date': self.date,
                              'options':[]})
        self.assertFalse(form.is_valid())

    def test_valid_answer_form(self):
        """ test to check if Answer form is valid """

        form = AnswerForm(instance=self.answer,data={
            'menu': self.answer.menu.pk,
            'menu_option' : self.answer.menu_option.pk,
            'comentaries': 'ensalada sin tomate',
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_answer_form(self):
        """ test to check if Answer form is invalid """

        form = AnswerForm(instance=self.answer,data={
            'menu': self.answer.menu.pk,
            'menu_option' : '',
            'comentaries': 'ensalada sin tomate',
            }
        )

        self.assertFalse(form.is_valid())
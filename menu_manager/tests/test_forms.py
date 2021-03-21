from django.test import TestCase
from menu_manager.forms import MenuForm, AnswerForm
from menu_manager.models import Option, Answer

class TestForms(TestCase):
    fixtures = ['fixtures_menu.json']

    def setUp(self):
        option = Option.objects.first()
        answer = Answer.objects.first()
        self.option = option
        self.answer = answer


    def test_invalid_menu_form(self):
        """ test to check if menu form is invalid """
        form = MenuForm(data={'start_date':'','options':[self.option.pk]})
        self.assertFalse(form.is_valid())

    def test_valid_menu_form(self):
        """ test to check if menu form is valid """
        form = MenuForm(data={'start_date':'2020-03-04',
                              'options':[self.option.pk]})
        self.assertTrue(form.is_valid())

    def test_valid_answer_form(self):
        """ test to check if Answer form is valid """
        form = AnswerForm(instance=self.answer,data={
            'menu': self.answer.menu.pk,
            'menu_option' : self.answer.menu_option.pk,
            'comentaries': 'ensalada sin tomate',
            }
        )

        self.assertTrue(form.is_valid())
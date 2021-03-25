from django.test import TestCase

from menu_manager.models import Option, Menu
from django.utils import timezone
from datetime import datetime, timedelta

class OptionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.option = Option.objects.create(
            meal = 'cerdo con arroz, ensalada y postre'
        )


    def test_it_has_information_fields(self):
        self.assertIsInstance(self.option.meal, str)

    def test_model_str_method(self):
        self.assertEqual(str(self.option), "cerdo con arroz, ensalada y postre")
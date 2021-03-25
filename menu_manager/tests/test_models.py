from django.test import TestCase

from menu_manager.models import Option


class ActorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.option = Option.objects.create(
            meal = 'cerdo con arroz, ensalada y postre'
        )


    def test_it_has_information_fields(self):
        self.assertIsInstance(self.option.meal, str)
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from menu_manager.views import *

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('menu_manager:index')
        self.assertEqual(resolve(url).func.view_class,IndexView)

    def test_option_list_url_is_resolved(self):
        url = reverse('menu_manager:option_list')
        self.assertEqual(resolve(url).func.view_class,OptionListView)

    def test_create_option_url_is_resolved(self):
        url = reverse('menu_manager:create_option')
        self.assertEqual(resolve(url).func.view_class,OptionMenuCreateView)

    def test_create_menu_url_is_resolved(self):
        url = reverse('menu_manager:create_menu')
        self.assertEqual(resolve(url).func.view_class,MenuCreateView)

    def test_update_menu_url_is_resolved(self):
        url = reverse('menu_manager:update_menu',args=['48a62b68-88c6-11eb-8dcd-0242ac130003'])
        self.assertEqual(resolve(url).func.view_class,MenuUpdateView)

    def test_menu_list_url_is_resolved(self):
        url = reverse('menu_manager:menu_list')
        self.assertEqual(resolve(url).func.view_class,MenuListView)

    def test_today_menu_list_url_is_resolved(self):
        url = reverse('menu_manager:today_menu',args=['48a62b68-88c6-11eb-8dcd-0242ac130003'])
        self.assertEqual(resolve(url).func.view_class,TodayMenuView)

    def test_results_url_is_resolved(self):
        url = reverse('menu_manager:results',args=['48a62b68-88c6-11eb-8dcd-0242ac130003'])
        self.assertEqual(resolve(url).func.view_class,AnswerListView)

    def test_answer_url_is_resolved(self):
        url = reverse('menu_manager:done')
        self.assertEqual(resolve(url).func.view_class,AnswerDone)




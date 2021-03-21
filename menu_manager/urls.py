from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path(
        'create_option/option_list',
        views.OptionListView.as_view(),
        name="option_list"
    ),
    path(
        'create_option',
        views.OptionMenuCreateView.as_view(),
        name='create_option'
    ),
    path(
        'create_menu',
        views.MenuCreateView.as_view(),
        name='create_menu'
    ),
    path(
        'update_menu/<uuid:menu_pk>',
        views.MenuUpdateView.as_view(),
        name='update_menu'
    ),
    path(
        'delete/<uuid:menu_pk>',
        views.MenuDeleteView.as_view(),
        name='delete_menu'
    ),
    path(
        'create_menu/menu_list',
        views.MenuListView.as_view(),
        name='menu_list'
    ),
    path(
        'menu/<uuid:answer_pk>',
        views.TodayMenuView.as_view(),
        name='today_menu'
    ),
    path(
        'results/<uuid:menu_pk>',
        views.AnswerListView.as_view(),
        name='results'
    ),
    path(
        'menu/answer_done',
        views.AnswerDone.as_view(),
        name='done'
    ),
]
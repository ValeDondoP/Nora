from django.conf.urls import url
from django.urls import path
from . import views




urlpatterns = [
    path('slack_bot',views.index,name='slack_bot'),
    path('slack/oauth/', views.slack_oauth,name='slack_oauth'),
    path('event/hook/', views.event_hook, name='event_hook'),
]
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic import ListView

from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
#from  menu_manager.tasks import *
from django.conf import settings
#import requests
import json
from django.http import HttpResponse
from .forms import *
from .models import *
from slack_bot.tasks import *
from django.contrib.sites.models import Site

# Create your views here.

class IndexView(
        LoginRequiredMixin,
        TemplateView,
    ):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       # a=send_message.delay()
       # print(a.ready())
        #current_site = Site.objects.get_current()
        #print(current_site)
        return context

class OptionListView(
        LoginRequiredMixin,
        ListView,
    ):
    model = Options
    template_name = 'web/option_list.html'


class OptionMenuCreateView(
        LoginRequiredMixin,
        TemplateView
    ):
    model = Options
    template_name = 'web/create_option.html'

    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = OptionFormSet(queryset=Options.objects.none())
        return self.render_to_response({'formset': formset})

    def post(self, *args, **kwargs):

        formset = OptionFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("menu_manager:option_list"))

        return self.render_to_response({'formset': formset})


class MenuCreateView(
        LoginRequiredMixin,
        CreateView,
):
    template_name = 'web/create_menu.html'
    form_class = MenuForm

    def get_success_url(self):
        return reverse_lazy(
            'menu_manager:menu_list'
        )

    def form_valid(self, form):
        form.save()
        return super(MenuCreateView, self).form_valid(form)


class MenuUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    model = Menu
    template_name = 'web/update_menu.html'
    form_class = MenuFormUpdate

    def get_object(self, *args, **kwargs):
        menu_pk = self.kwargs.get('menu_pk')
        menu = Menu.objects.get(id=menu_pk)
        return menu

    def get_success_url(self):
        return reverse_lazy(
            'menu_manager:menu_list'
        )

    def form_valid(self, form):
        form.save()
        return super(MenuUpdateView, self).form_valid(form)


class MenuListView(
    LoginRequiredMixin,
    ListView,
):
    model = Menu
    template_name = "web/menu_list.html"


class TodayMenuView(
    UpdateView,
):
    model = Answer
    template_name = 'web/today_menu.html'
    form_class = AnswerForm

    def get_object(self, *args, **kwargs):
        answer_pk = self.kwargs.get('answer_pk')
        answer = Answer.objects.get(pk=answer_pk)
        return answer

    def get_success_url(self):
        return reverse_lazy(
            'menu_manager:menu_list'
        )

    def form_valid(self, form):
        form.save()
        return super(TodayMenuView, self).form_valid(form)


class AnswerListView(
    LoginRequiredMixin,
    ListView,
):
    model = Answer
    template_name = "web/answer_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_pk =  self.kwargs.get('menu_pk')
        context['menu'] = Menu.objects.get(pk=menu_pk)
        return context
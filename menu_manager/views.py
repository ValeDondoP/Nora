from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic import ListView

from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404



from django.conf import settings


from .forms import (
    OptionFormSet,
    MenuForm,
    MenuFormUpdate,
    AnswerForm
)
from .models import (
    Menu,
    Option,
    Answer,
    Employee
)

# Create your views here.

class IndexView(
        LoginRequiredMixin,
        TemplateView,
    ):
    """
    Displays the home page of NoraApp
    """
    template_name = 'web/index.html'


class OptionListView(
        LoginRequiredMixin,
        ListView,
    ):
    model = Option
    template_name = 'web/option_list.html'


class OptionMenuCreateView(
        LoginRequiredMixin,
        TemplateView
    ):
    """Options Creation View
    Display a formset to create multiple options meals
    """
    model = Option
    template_name = 'web/create_option.html'

    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = OptionFormSet(queryset=Option.objects.none())
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
    """Menu Creation View
    Display a forms to create a menu with start_date and options to choose
    """
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
    """Menu Update View
    Display a forms to update an existing  menu with start_date and options to choose
    """
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


class MenuDeleteView(
        LoginRequiredMixin,
        UpdateView,
    ):
    """Menu Delete View
    Delete an existing menu
    """
    model = Menu

    def get_success_url(self):
        return reverse_lazy(
            'menu_manager:menu_list'
        )

    def get_object(self, *args, **kwargs):
        menu_pk = self.kwargs.get('menu_pk')
        menu = Menu.objects.get(id=menu_pk)
        return menu

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() # get object
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url) #redirect


class MenuListView(
        LoginRequiredMixin,
        ListView,
    ):
    """
    Display a list of all menus that the user creates
    """
    model = Menu
    template_name = "web/menu_list.html"
    ordering = ['-start_date']


class TodayMenuView(
        UpdateView,
    ):
    """
    Display a form with todays menu options, it is not shown after 11 ctl
    """
    model = Answer
    template_name = 'web/today_menu.html'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hour = timezone.localtime(timezone.now()).hour
        minutes = timezone.localtime(timezone.now()).minute
        print(hour)
        # menu available until 11
        if hour < 11  and hour >= 8:
            context['is_active'] = True
        elif hour == 11 and minute == 0:
            context['is_active'] = True
        return context

    def get_object(self, *args, **kwargs):
        answer_pk = self.kwargs.get('answer_pk')
        answer = Answer.objects.get(pk=answer_pk)
        return answer

    def get_success_url(self):
        return reverse_lazy(
            'menu_manager:done'
        )

    def form_valid(self, form):
        form.save()
        return super(TodayMenuView, self).form_valid(form)


class AnswerListView(
        LoginRequiredMixin,
        ListView,
    ):
    """
    Display a list of all answers from employees to specific menu
    """
    model = Answer
    template_name = "web/answer_list.html"

    def get_queryset(self):
        menu_pk = self.kwargs['menu_pk']
        qs = super(AnswerListView, self).get_queryset().filter(menu=Menu.objects.get(pk=menu_pk))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_pk =  self.kwargs.get('menu_pk')
        context['menu'] = Menu.objects.get(pk=menu_pk)
        return context


class AnswerDone(TemplateView):
    """
    Display a it's donde message to employee
    """
    template_name = 'web/menu_answer_done.html'

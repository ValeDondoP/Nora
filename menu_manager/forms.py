import datetime
from datetime import timedelta

from decimal import Decimal
from django import forms
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils import timezone
from django_select2.forms import Select2Widget, Select2MultipleWidget
from bootstrap_datepicker_plus import DatePickerInput

from .models import (
    Option,
    Menu,
    Answer,

)


"""Form used to create a multiples options menu"""
OptionFormSet = modelformset_factory(
    Option, fields=("meal",), extra=1
)

class MenuForm(ModelForm):
    """Form used to create a menu to send a certain date"""

    options =  forms.ModelMultipleChoiceField(
        required=True,
        widget=Select2MultipleWidget(),
        queryset=Option.objects.all(),
        label='Opciones',
    )
    class Meta:
        model = Menu
        fields = ['start_date',]


        labels = {
            'start_date': 'Fecha de Envío',
        }

        widgets = {
            'start_date': DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'minDate': (datetime.datetime.today()).strftime('%Y-%m-%d 00:00:00'),
                }
            )
        }

    def save(self, *args, **kwargs):
        menu = super().save(*args, **kwargs)

        # Save option's menu
        menu.options.set(self.cleaned_data['options'])
        menu.save()

        return menu

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if 'start_date' in cleaned_data:
            start_date =  cleaned_data['start_date']
            today = timezone.now().date()
            if start_date and  start_date < today:
                msg = 'No es posible agendar menus antes del día de hoy'
                self.add_error('start_date', msg)
        return self.cleaned_data


class MenuFormUpdate(ModelForm):
    """Form used to update a menu """

    options =  forms.ModelMultipleChoiceField(
        required=True,
        widget=Select2MultipleWidget(),
        queryset=Option.objects.all(),
    )
    class Meta:
        model = Menu
        fields = ['start_date',]

        widgets = {
            'start_date': DatePickerInput(format='%Y-%m-%d'),
            }
    def __init__(self, *args, **kwargs):
        super(MenuFormUpdate,self).__init__(*args, **kwargs)
        menu = self.instance
        self.fields['start_date'].initial = menu.start_date
        self.fields['options'].initial = menu.options.all()

    def save(self, *args, **kwargs):
        menu = super().save(*args, **kwargs)

        # Save option's menu
        menu.options.set(self.cleaned_data['options'])
        menu.save()
        return menu

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if 'start_date' in cleaned_data:
            start_date =  cleaned_data['start_date']
            today = timezone.now().date()
            if start_date and  start_date < today:
                msg = 'No es posible agendar menus antes del día de hoy'
                self.add_error('start_date', msg)
        return self.cleaned_data


class AnswerForm(forms.ModelForm):
    """Form used save the option that the user select"""
    class Meta:
        model = Answer
        fields = (
            'menu',
            'menu_option',
            'employee',
            'comentaries',
        )

    def __init__(self, *args, **kwargs):
        super(AnswerForm,self).__init__(*args, **kwargs)
        answer = self.instance
        # menu and employee already set
        self.fields['menu'].initial = answer.menu
        self.fields['menu'].widget = forms.HiddenInput()

        self.fields['employee'].initial = answer.employee
        self.fields['employee'].widget = forms.HiddenInput()
        self.fields['menu_option'] = forms.ModelChoiceField(
                                            queryset=answer.menu.options.all(),
                                      )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if 'employee' in cleaned_data:
            employee =  cleaned_data['employee']
            if employee != self.instance.employee :
                msg = 'No es posible agendar respuesta'
                self.add_error('employee', msg)
        return self.cleaned_data
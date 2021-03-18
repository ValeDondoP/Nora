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
    Options,
    Menu,
    Answer,

)

class OptionForm(ModelForm):
    class Meta:
        model = Options

        fields = (
            'meal',
        )

OptionFormSet = modelformset_factory(
    Options, fields=("meal",), extra=1
)

class MenuForm(ModelForm):
    options =  forms.ModelMultipleChoiceField(
        required=True,
        widget=Select2MultipleWidget(),
        queryset=Options.objects.all(),
    )
    class Meta:
        model = Menu
        fields = ['start_date',]

        widgets = {
            'start_date': DatePickerInput(format='%Y-%m-%d'),
            }

    def save(self, *args, **kwargs):
        menu = super().save(*args, **kwargs)

        # Save option's menu
        menu.options.set(self.cleaned_data['options'])
        menu.save()

        return menu


class MenuFormUpdate(ModelForm):
    options =  forms.ModelMultipleChoiceField(
        required=True,
        widget=Select2MultipleWidget(),
        queryset=Options.objects.all(),
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


class AnswerForm(forms.ModelForm):

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
        answer=self.instance
        self.fields['menu'].initial = answer.menu
        self.fields['menu'].widget = forms.HiddenInput()

        self.fields['employee'].initial = answer.employee
        self.fields['employee'].widget = forms.HiddenInput()
        self.fields['menu_option'] = forms.ModelChoiceField(
                                            queryset=answer.menu.options.all(),
                                      )

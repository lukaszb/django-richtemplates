import logging
import django_filters

from django import forms
from django.db.models import Q

from richtemplates.forms import LimitingModelForm
from richtemplates.examples.models import Task, Status, Priority, Project

RATING = [(i, u'%d' % i) for i in xrange(1,6)]

class ContactForm(forms.Form):
    """
    Example of boring contact form.
    """
    username = forms.CharField(min_length=2, max_length=16)
    content = forms.CharField(min_length=10, max_length=3000, widget=forms.Textarea)
    rating = forms.ChoiceField(choices=RATING, initial=1)
    email = forms.EmailField(required=False)

class TaskForm(LimitingModelForm):
    class Meta:
        model = Task
        choices_limiting_fields = ['project']

    class Media:
        css = {'all': ['richtemplates/css/monoarea.css']}

class TaskFilterForm(LimitingModelForm):
    task_id = forms.IntegerField("#", min_value=1)
    created_from = forms.DateTimeField(label="Created from",
        widget=forms.DateTimeInput(attrs={'class': 'datepicker'}),
        help_text='YYYY-MM-DD')
    created_to = forms.DateTimeField(label="Created to",
        widget=forms.DateTimeInput(attrs={'class': 'datepicker'}),
        help_text='YYYY-MM-DD')
    
    def __init__(self, *args, **kwargs):
        ret = super(TaskFilterForm, self).__init__(*args, **kwargs)
        for field in self.base_fields.values():
            field.required = False
        return ret

    class Meta:
        model = Task
        choices_limiting_fields = ['project']
        fields = ['status', 'priority', 'summary', 'project']

    def get_filters(self):
        """
        Returns ``Q`` object representing combined filters.
        """
        qset = Q()

        if self.is_valid():
            data = self.cleaned_data
            if data['task_id']:
                qset = qset & Q(id=data['task_id'])
        else:
            logging.error("TaskFilterForm contains errors: %s"
                % self.erros)
        return qset

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['id', 'status', 'priority']

    


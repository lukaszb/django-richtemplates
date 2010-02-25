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

def TaskFilter(data=None, queryset=Task.objects.all(), project=None):
    """
    Factory method which returns ``FilterSet`` for given project.
    """
    class TaskFilter(django_filters.FilterSet):
        class Meta:
            model = Task
            fields = ['id', 'status', 'priority']

        def __init__(self, *args, **kwargs):
            super(TaskFilter, self).__init__(*args, **kwargs)
            if project:
                self.filters['status'].extra.update(
                    {'queryset': project.status_set.all()})
                self.filters['priority'].extra.update(
                    {'queryset': project.priority_set.all()})
    filterset = TaskFilter(data, queryset)
    return filterset


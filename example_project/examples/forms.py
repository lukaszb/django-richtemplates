import django_filters

from django import forms
from django.contrib.auth.models import Group

from richtemplates.forms import LimitingModelForm, UserByNameField
from richtemplates.widgets import RichCheckboxSelectMultiple
from richtemplates import settings as richtemplates_settings
from examples.models import Task

RATING = [(i, u'%d' % i) for i in xrange(1,6)]

class ContactForm(forms.Form):
    """
    Example of boring contact form.
    """
    username = UserByNameField(min_length=2, max_length=16)
    content = forms.CharField(min_length=10, max_length=3000,
        widget=forms.Textarea,
        help_text="Lorem ipsum dolor sit amet. " * 10)
    rating = forms.ChoiceField(choices=RATING, initial=1)
    email = forms.EmailField(required=False)
    deadline = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        help_text="Format: YYYY-MM-DD")
    action = forms.ChoiceField(choices=[(1, 'foo'), (2, 'bar')],
        widget=forms.RadioSelect)
    how_to_reach_me = forms.MultipleChoiceField(choices=(
            ('email', 'Via Email'),
            ('phone', 'Via phone'),
        ), initial=['email'], required=False,
        widget = RichCheckboxSelectMultiple
    )

def unslugify(value):
    return value.replace('_', ' ').replace('-', ' ').capitalize()

class MultipleChoicesForm(forms.Form):
    CHOICES = ((key, unslugify(key)) for key in (
        ('view_project'),
        ('edit_project'),
        ('add_project'),
        ('delete_project'),
        ('view_task'),
        ('edit_task'),
        ('add_task'),
        ('delete_task'),
        ('view_user'),
        ('edit_user'),
        ('add_user'),
        ('delete_user'),
        ('view_group'),
        ('edit_group'),
        ('add_group'),
        ('delete_group'),
    ))
    fake_permissions = forms.MultipleChoiceField(choices=CHOICES,
        initial = ['view_project', 'edit_project', 'add_task', 'delete_task'],
        required = False,
        widget = RichCheckboxSelectMultiple)


class UserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(Group.objects.all())

class TaskForm(LimitingModelForm):
    class Meta:
        model = Task
        choices_limiting_fields = ['project']

    class Media:
        css = {'all': [richtemplates_settings.MEDIA_URL + 'css/monoarea.css']}

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


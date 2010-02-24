from django import forms

from richtemplates.forms import LimitingModelForm
from richtemplates.examples.models import Task

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


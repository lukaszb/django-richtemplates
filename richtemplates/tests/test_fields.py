from django.test import TestCase
from django import forms
from django.contrib.auth.models import User

from richtemplates.fields import ModelByNameField
from richtemplates.forms import LimitingModelForm

class TestForm(forms.Form):
    user = ModelByNameField(queryset=User.objects.all(), attr='username')

class TestFormLimited(LimitingModelForm):
    user = ModelByNameField(queryset=User.objects.all(), attr='username')

    class Meta:
        model = User

class ModelByNameFieldTest(TestCase):

    def test_queryset_laziness(self):
        form = TestForm()
        user_field = form.fields['user']
        init_count = user_field.queryset.count()
        User.objects.create_user('test_queryset_laziness', 'foo@bar.baz', '')
        after_count = user_field.queryset.count()
        self.assertTrue(after_count > init_count)

    def test_queryset_laziness_limiting(self):
        form = TestFormLimited(instance=User())
        user_field = form.fields['user']
        init_count = user_field.queryset.count()
        User.objects.create_user('test_queryset_laziness_limiting',
            'foo@bar.baz', '')
        after_count = user_field.queryset.count()
        self.assertTrue(after_count > init_count)


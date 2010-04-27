from django import forms
from django.contrib.auth.models import User

class RestructuredTextAreaField(forms.CharField):

    widget = forms.Textarea(attrs={'cols': '80', 'rows': '10', 'wrap': 'off'})

class UserByNameField(forms.CharField):
    """
    Allows to choose user by simple typing his or her
    name instead of picking up from <select> tag.
    """
    def __init__(self, queryset=User.objects.all(), *args, **kwargs):
        super(UserByNameField, self).__init__(*args, **kwargs)
        if callable(queryset):
            self.queryset = queryset
        self.queryset = queryset

    def clean(self, value):
        """
        Returns user for whom task is beign assigned.
        """
        # Firstly, we have to clean as normal CharField
        value = super(UserByNameField, self).clean(value)
        # Now do the magic
        username = value.strip()
        if username == '':
            return None
        try:
            user = self.queryset.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No user found!")
        return user

class ModelByNameField(forms.CharField):
    """
    """
    def __init__(self, queryset, field='name', *args, **kwargs):
        super(ModelByNameField, self).__init__(*args, **kwargs)
        self.queryset = callable(queryset) and queryset() or queryset
        self.field = field

    def clean(self, value):
        """
        Returns instance of model class of the given queryset.
        """
        # Clean as normal CharField first
        value = super(ModelByNameField, self).clean(value)
        value = value.strip()
        if value == '':
            return None
        try:
            instance = self.queryset.get(**{self.field: value})
        except self.queryset.model.DoesNotExist:
            raise forms.ValidationError("No object found")
        return instance


from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from richtemplates.utils import LazyProperty

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
            raise forms.ValidationError(_("No user found!"))
        return user

class ModelByNameField(forms.CharField):
    """
    This field acts like normal CharField but at the time it is being cleaned
    it would try to fetch instance from the given ``queryset``. Cleaned value
    is used in a undelying query.

    :param: queryset - ``QuerySet`` object specyfing model to be fetched; may be
      callable
    :param: attr - attribute used to fetch instance from the ``queryset``

    Example::

       >>> field = ModelByNameField(queryset=User.objects.all, attr='username')
       >>> field.clean('admin')

    Above code returns User instance with 'admin' username or raises
    ``forms.ValidationError`` if that user does not exist. Note that we pass not
    yet called ``User.objects.all`` function and we specify attribute
    ``username`` which is used by ``clean`` method to fetch proper instance.
    """
    def __init__(self, queryset, attr='name', *args, **kwargs):
        super(ModelByNameField, self).__init__(*args, **kwargs)
        self._queryset = queryset
        self.attr = attr

    @LazyProperty
    def queryset(self):
        if callable(self._queryset):
            return self._queryset()
        return self._queryset

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
            instance = self.queryset.get(**{self.attr: value})
        except self.queryset.model.DoesNotExist:
            raise forms.ValidationError(_("No object found"))
        return instance


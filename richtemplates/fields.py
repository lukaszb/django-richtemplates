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
        self.queryset = queryset
        super(UserByNameField, self).__init__(*args, **kwargs)

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
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No user found!")
        logging.debug("Returns UserByNameField: %s" % user)
        return user


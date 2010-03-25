import richtemplates.settings

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from annoying.decorators import signals
from richtemplates.utils import get_user_profile_model

class UserProfile(models.Model):
    """
    This class would be abstract if ``AUTH_PROFILE_MODULE`` is not equal to
    ``richtemplates.UserProfile`` (this class) as one may use his own, custom
    profile. If so, it is possible to simply extend this class or leave it at
    all.
    """
    user = models.ForeignKey(User, unique=True)
    skin = models.CharField(max_length=128,
        default=richtemplates.settings.DEFAULT_SKIN)

    class Meta:
        abstract = getattr(settings, 'AUTH_PROFILE_MODULE',
             '') != 'richtemplates.UserProfile'

@signals.post_save(sender=User)
def new_richtemplates_profile(instance, **kwargs):
    if kwargs['created'] is True:
        _ProfileModel = get_user_profile_model()
        _ProfileModel is not None and _ProfileModel.objects.create(
            user = instance,
        )


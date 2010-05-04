from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from annoying.decorators import signals
from richtemplates.utils import get_user_profile_model
from richtemplates import settings as richtemplates_settings

class UserProfile(models.Model):
    """
    This class would be abstract if ``AUTH_PROFILE_MODULE`` is not equal to
    ``richtemplates.UserProfile`` (this class) as one may use his own, custom
    profile. If so, it is possible to simply extend this class or leave it at
    all.
    """
    user = models.ForeignKey(User, verbose_name=_('user'), unique=True)
    skin = models.CharField(max_length=128, verbose_name=('skin'),
        default=richtemplates_settings.DEFAULT_SKIN,
        help_text=_("Skin used on the site"))
    code_style = models.CharField(_('Codes style'), max_length=128,
        default=richtemplates_settings.DEFAULT_CODE_STYLE,
        help_text=_("Style used to show code snippets"))

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


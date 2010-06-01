from django.db.models import signals
from django.contrib.auth.models import User

from richtemplates.utils import get_user_profile_model

def new_richtemplates_profile(instance, **kwargs):
    if kwargs['created'] is True:
        _ProfileModel = get_user_profile_model()
        if _ProfileModel is not None:
            _ProfileModel.objects.create(
                user = instance,
            )

signals.post_save(new_richtemplates_profile, sender=User,
    dispatch_uid="richtemplates.listeners.new_richtemplates_profile")


import logging

from django.db.models import signals
from django.db import DatabaseError, IntegrityError
from django.contrib.auth.models import User

from richtemplates.utils import get_user_profile_model

def new_richtemplates_profile(instance, **kwargs):
    if kwargs['created'] is True:
        UserProfile = get_user_profile_model()
        if UserProfile is not None:
            try:
                # We run get_or_create instead of create as there may be other
                # handlers which would automaticaly create profiles
                UserProfile.objects.get_or_create(
                    user = instance,
                )
                logging.debug("New profile created for user %s" % instance)
            except (DatabaseError, IntegrityError), err:
                logging.warning("Richtemplates tried to create profile for new "
                                "user %s but it seems there is already one or "
                                "profile table does not exist. "
                                "Original error: %s" % (instance, err))
                logging.warning("Consider running syncdb again after issue is "
                                "resolved")


def start_listening():
    signals.post_save.connect(new_richtemplates_profile, sender=User,
        dispatch_uid="richtemplates.listeners.new_richtemplates_profile")


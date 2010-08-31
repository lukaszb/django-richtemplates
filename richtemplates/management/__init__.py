import sys
import logging

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Count
from django.db.models import signals
from django.db.models.loading import get_app

from richtemplates.utils import get_user_profile_model


PROFILE_APP = None

def put_missing_userprofiles(sender, **kwargs):
    """
    If user profile model is defined at ``settings.AUTH_PROFILE_MODULE``
    richtemplates would try to find out if there are missing profiles
    and would ask to create them if necessary.
    """
    UserProfile = get_user_profile_model()
    if UserProfile:
        try:
            global PROFILE_APP
            PROFILE_APP = get_app(UserProfile._meta.app_label)
        except ImproperlyConfigured:
            pass
        users_count = User.objects.count()
        profiles_count = UserProfile.objects.count()
        if users_count > profiles_count:
            if kwargs['interactive'] is True:
                msg = "There are %d User objects without profiles"\
                    % (users_count - profiles_count)
                logging.info(msg)
                answer = ''
                while answer.lower() not in ('yes', 'no'):
                    prompt = "Create missing profiles? [yes/no]: "
                    try:
                        answer = raw_input(prompt).lower()
                    except KeyboardInterrupt:
                        sys.stderr.write("\nInterrupted by user - taken "
                            "as 'no'\n")
                        answer = 'no'
                if answer == 'yes':
                    rel_profile_name = UserProfile._meta.object_name.lower()
                    users_without_profile = User.objects\
                        .annotate(profile_count=Count(rel_profile_name))\
                        .filter(profile_count=0)
                    for user in users_without_profile:
                        UserProfile.objects.create(user=user)
                        if kwargs['verbosity'] >= 1:
                            print "[INFO] Created profile for user %s" % user


# Connect signal only if we could find an app
if PROFILE_APP:
    signals.post_syncdb.connect(put_missing_userprofiles, sender=PROFILE_APP,
        dispatch_uid="richtemplates.management.put_missing_userprofiles")


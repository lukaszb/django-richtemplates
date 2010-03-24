import sys
import logging

from django.contrib.auth.models import User
from django.db.models import Count

from annoying.decorators import signals
from richtemplates import models as richtemplates_app
from richtemplates.models import UserProfile

@signals.post_syncdb(sender=richtemplates_app)
def richtemplates_syncdb(**kwargs):
    if UserProfile._meta.abstract is False:
        users_count = User.objects.count()
        profiles_count = UserProfile.objects.count()
        if users_count > profiles_count:
            if kwargs['interactive'] is True:
                msg = "There are %d User objects without profiles"\
                    % (users_count - profiles_count)
                logging.info(msg)
                answer = ''
                while answer.lower() not in ('yes', 'no'):
                    prompt = "Create lacking profiles? [yes/no]: "
                    try:
                        answer = raw_input(prompt).lower()
                    except KeyboardInterrupt:
                        sys.stderr.write("\nInterrupted by user!\n")
                        sys.exit(1)
                if answer == 'yes':
                    users_without_profile = User.objects\
                        .annotate(profile_count=Count('userprofile'))\
                        .filter(profile_count=0)
                    for user in users_without_profile:
                        UserProfile.objects.create(user=user)
                        if kwargs['verbosity'] == 2:
                            print "[INFO] Created profile for user %s" % user


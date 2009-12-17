from django.core.management.base import LabelCommand, CommandError
from richtemplates.management import rt_init
from optparse import make_option

import logging
import pprint

class Command(LabelCommand):
    help = u"Copies richtemplates media directory inside target directory."
    args = 'MEDIA_DIR'

    def handle_label(self, label='media', **options):
        """
        Creates initial templates - copy one of richtemplates'
        profile into directory given as ``label`` parameter.
        """

        rt_init.init_media(label)




from django.core.management.base import LabelCommand, CommandError
from richtemplates.management import rt_init
from optparse import make_option

import logging
import pprint

class Command(LabelCommand):
    help = """
        Initializes 'template' directory and populates it
        with templates from richtemplates/templates source.
    """
    args = 'TEMPLATES_DIR'
    option_list = LabelCommand.option_list + (
        make_option('-p', '--profile', dest='profile', default='basic',
            help='Profile of the selected templates.'),
        make_option('-m', '--media', dest='media',
            help='If specified, will try to copy richtemplates\' media'
                ' into directory at parameter of this option.'),
        make_option('--copy-richtemplates', dest='copy_richtemplates',
            default=False, action='store_true',
            help='Copies internal templates of richtemplates into '
                 'TEMPLATES_DIR/richtemplates'),
    )

    def handle_label(self, label='templates', **options):
        """
        Creates initial templates - copy one of richtemplates'
        profile into directory given as ``label`` parameter.
        """
        
        if options['media']:
            rt_init.init_media(options['media'])
        rt_init.init(label, options['profile'])



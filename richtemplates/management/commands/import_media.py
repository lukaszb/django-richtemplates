import os
import logging
import richtemplates

from optparse import make_option

from django.conf import settings
from django.core.management.base import LabelCommand, CommandError
from django.template.defaultfilters import slugify
from django.utils.importlib import import_module

from richtemplates.management import rt_init, submedia
from richtemplates.management.helpers import copy_dir_helper, make_writeable,\
    get_settings_as_dict

class Command(LabelCommand):
    help =  '\n'.join(["Copies 'media' directory from django pluggable app into this",
            "project. Makes use of MEDIA_URL, MEDIA_ROOT, ADMIN_MEDIA_PREFIX",
            "and any other similar, corresponding-to-app settings.\n",
            "For example, if you set app_name option to 'richtemplates' and ",
            "there is RICHTEMPLATES_MEDIA_PREFIX set to ",
            "\"MEDIA_URL + '/richtemplates/'\" (without doublequotes), and ",
            "css/js files within 'richtemplates/media' directory contain ",
            "\"{{ RICHTEMPLATES_MEDIA_PREFIX }} it will be replaced with ",
            "these from settings module. Files would be placed at ",
            os.path.join(settings.MEDIA_ROOT, '<app>'),
        ])
    args = '[apps]'
    requires_model_validation = False
    option_list = LabelCommand.option_list + (
        make_option('--media-root', dest='media_root',
            default=settings.MEDIA_ROOT,
            help='Override MEDIA_ROOT setting.'),
        make_option('--without-setting-variable', action='store_true',
            dest='without_setting_variable', default=False,
            help='If specified, command will ommit verification if '\
                 'proper variable exists at settings module.'),
        make_option('--fail-silently', action='store_true',
            dest='fail_siltently', default=False,
            help="If specified, won't raise exception if app "
                 "does not have 'media' directory to import."),
        )

    def get_version(self):
        return richtemplates.get_version()

    def handle_label(self, app=None, **options):
        if app is None:
            raise CommandError("Specify at least one app")
        if app not in settings.INSTALLED_APPS:
            raise CommandError("%s not found at INSTALLED_APPS" % app)
        MEDIA_ROOT = os.path.abspath(options['media_root'])
        if options['without_setting_variable'] is False:
            key = (slugify(app) + '_MEDIA_PREFIX').upper()
            if not key in get_settings_as_dict(settings).keys():
                raise CommandError("Either set %s variable in your settings "
                    "or run command with --without-setting-variable option."
                    % key)
        dst = os.path.join(MEDIA_ROOT, app)
        if os.path.exists(MEDIA_ROOT):
            if not os.path.isdir(MEDIA_ROOT):
                raise CommandError("%s is not a directory" % MEDIA_ROOT)
            if os.path.exists(dst):
                raise CommandError("%s already exists" % dst)
        else:
            os.mkdir(MEDIA_ROOT)
        try:
            app_module = import_module(app)
        except ImportError:
            raise CommandError("Cannot find app %s" % app)
        app_path = app_module.__path__[0]
        app_media_dir = os.path.abspath(os.path.join(app_path, 'media'))
        if not os.path.isdir(app_media_dir) and \
            options['fail_siltently'] is False:
            raise CommandError("Specified app has no 'media' directory!")
        copy_dir_helper(app_media_dir, dst)
        make_writeable(MEDIA_ROOT)

        submedia.submedia_files(dst)


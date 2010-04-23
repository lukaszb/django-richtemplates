import os
import richtemplates

from optparse import make_option

from django.conf import settings
from django.core.management.base import LabelCommand, CommandError
from django.utils.importlib import import_module

from richtemplates.management.helpers import copy_dir_helper, make_writeable

class Command(LabelCommand):
    help = """
    Copies ``media`` directory from django pluggable app into this project.

    If ``media`` directory would containt subdirectory called same as this
    application's ``app_label``, this subdirectory would become source
    directory (i.e. this would import media from excellent `django-admin-tools
    <http://bitbucket.org/izi/django-admin-tools/>`_ properly).

    Source directory is put into ``media`` directory inside the project. If
    this destination directory does not exist it would be created.

    **Synopsis**

    .. code-block:: bash

       ./manage.py import_media [options] app [app2] [app3] ...

    **Options**

    ``--fail-silently``
      *Default*: ``False``

      Turning on would not raise exception if specified ``app`` does not have
      ``media`` directory.

    ``--force``
       *Default*: ``False``

       By default, if destination directory already exists, ``CommandError``
       would be raised. By turning this flag on check is not made.

    ``--media-root``
       *Default*: same as ``django.settings.MEDIA_ROOT``

       This is destination directory. All source directories would be copied
       as *subdirectories* into this directory.

    """
    __doc__ = help

    args = 'app [app2] [app3]'
    requires_model_validation = False
    option_list = LabelCommand.option_list + (
        make_option('--media-root', dest='media_root',
            default=settings.MEDIA_ROOT,
            help='Override MEDIA_ROOT setting.'),
        make_option('--fail-silently', action='store_true',
            dest='fail_siltently', default=False,
            help="If specified, won't raise exception if app "
                 "does not have 'media' directory to import."),
        make_option('-f', '--force', action='store_true',
            dest='force', default=False,
            help='With this flag command will not check for existence '
                 'of specified apps (media folders will be overriden).'),
        )

    def get_version(self):
        return richtemplates.get_version()

    def handle_label(self, app=None, **options):
        if app is None:
            raise CommandError("Specify at least one app")
        if app not in settings.INSTALLED_APPS:
            raise CommandError("%s not found at INSTALLED_APPS" % app)
        MEDIA_ROOT = os.path.abspath(options['media_root'])

        dst = os.path.join(MEDIA_ROOT, app)
        if os.path.exists(MEDIA_ROOT):
            if not os.path.isdir(MEDIA_ROOT):
                raise CommandError("%s is not a directory" % MEDIA_ROOT)
            if os.path.exists(dst) and options['force'] is False:
                raise CommandError("%s already exists" % dst)
        else:
            os.mkdir(MEDIA_ROOT)
        try:
            app_module = import_module(app)
        except ImportError:
            raise CommandError("Cannot find app %s" % app)
        app_path = app_module.__path__[0]
        app_dir = os.path.basename(app_path)
        app_media_dir = os.path.abspath(os.path.join(app_path, 'media'))
        _inner = os.path.join(app_media_dir, app_dir)
        if os.path.isdir(_inner):
            #logging.debug("Seems that %s has main media subdirectory, will "
            #    "use it (%s)" % (app_module.__name__, _inner))
            app_media_dir = _inner

        if not os.path.isdir(app_media_dir) and \
            options['fail_siltently'] is False:
            raise CommandError("Specified app '%s' has no 'media' directory!"
                % app)
        copy_dir_helper(app_media_dir, dst, force=options['force'])
        make_writeable(MEDIA_ROOT)

        # Replaces django template variables with
        # ones founded in your settings file
        # submedia.submedia_files(dst)
        # Turning off as implementation was bad design decision


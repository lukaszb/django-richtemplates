import os
import shutil
import inspect
import logging

from django.core.management.base import _make_writeable, CommandError

def copy_dir_helper(src, dst, force=False):
    """
    Convenience method to copy directory from source
    to defined destination. You have to change permissions
    if needed.
    """
    if not os.path.isdir(src):
        raise CommandError("Source directory %s does not exists" % src)
    if os.path.exists(dst):
        if force:
            logging.debug('Force mode was turned on. Removing %s' % dst)
            shutil.rmtree(dst)
        else:
            raise CommandError("Target %s already exists" % dst)
    shutil.copytree(src, dst)
    logging.info("Copied %s into %s" % (src, dst))
    make_writeable(dst)

def make_writeable(target):
    """
    Changes permissions for the target using internal Django function.
    """
    for dir, subdirs, files in os.walk(target):
        file_names = [os.path.join(dir, fn) for fn in files]
        subdir_names = [os.path.join(dir, subdir) for subdir in subdirs]
        entries = file_names + subdir_names
        for entry in entries:
            _make_writeable(entry)

def get_settings_as_dict(settings_module):
    """
    Returns given module as dict object with
    keys taken from settings_module. Only
    members with uppered names are returned.
    """
    return dict((key, val) for key, val in inspect.getmembers(settings_module)\
        if key == key.upper())


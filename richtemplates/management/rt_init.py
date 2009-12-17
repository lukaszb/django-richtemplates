import os
import shutil
import logging
import richtemplates

from django.core.management.base import copy_helper, _make_writeable, CommandError

rt_src_dir = os.path.join(richtemplates.__path__[0])
rt_templates_dir = os.path.join(rt_src_dir, 'templates')
rt_templates_profiles_dir = os.path.join(rt_src_dir, 'templates_profiles')
rt_media_dir = os.path.join(rt_src_dir, 'media')

def init_media(target_dir):
    """
    Copies richtemplates media file into target_dir/richtemplates.
    """
    if not os.path.isdir(target_dir):
        logging.debug("Will create %s directory." % target_dir)
        os.mkdir(target_dir)
    dst = os.path.abspath(os.path.join(target_dir, 'richtemplates'))
    copy_dir_helper(rt_media_dir, dst)
    make_writeable(target_dir)

def init(target_dir, profile):
    """
    Copies templates profile from templates_profiles
    located within richtemplates source directory
    into target_dir. If target_dir exists CommandError
    is raised.
    """
    profile_dir = os.path.join(rt_templates_profiles_dir, profile)
    copy_dir_helper(profile_dir, target_dir)
    make_writeable(target_dir)

def copy_dir_helper(src, dst):
    """
    Convenience method to copy directory from source
    to defined destination. You have to change permissions
    if needed.
    """
    if not os.path.isdir(src):
        raise CommandError("Source directory %s does not exists" % src)
    if os.path.exists(dst):
        raise CommandError("Target %s already exists" % dst)
    shutil.copytree(src, dst)
    logging.debug("Copied %s into %s" % (src, dst))


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


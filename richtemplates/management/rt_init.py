import os
import shutil
import logging
import richtemplates

from django.core.management.base import _make_writeable, CommandError

from richtemplates.management.helpers import copy_dir_helper

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

def init(target_dir, profile):
    """
    Copies templates profile from templates_profiles
    located within richtemplates source directory
    into target_dir. If target_dir exists CommandError
    is raised.
    """
    profile_dir = os.path.join(rt_templates_profiles_dir, profile)
    copy_dir_helper(profile_dir, target_dir)



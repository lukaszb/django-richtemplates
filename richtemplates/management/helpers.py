import os
import shutil
import inspect
import logging

from django.core.management.base import _make_writeable, CommandError
from shutil import copy2, copystat, Error
from richtemplates.extras.progressbar import ProgressBar

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
    copytree(src, dst, draw_pbar=True)
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

def copytree(src, dst, symlinks=False, ignore=None, draw_pbar=False):
    """
    Copies directory from ``src`` into ``dst``.

    Codes taken from shutil module, with some progressbar sugar.
    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    try:
        pbar = ProgressBar(color='GREEN', width=40)
    except:
        pbar = None
        draw_pbar = False
    total = len(names)

    for i in xrange(total):
        name, perc = names[i], 100 * i / total
        draw_pbar and pbar.render(perc)
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except OSError, why:
        try:
            from shutil import WindowsError
            WindowsError # For pylint
        except ImportError:
            WindowsError = None
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error, errors
    draw_pbar and pbar.render(100, "Done")


import os
import os.path

from django.conf import settings
from django.template import Template, Context
from richtemplates.management.helpers import get_settings_as_dict

media_suffix_list = ['js', 'css']

def is_media_file(filename):
    ext = filename.split('.')[-1]
    if ext.lower() in media_suffix_list:
        return True
    return False

def subfile(filename, context):
    """
    Rewrites file rendering it with given context
    using Template.render method.
    """
    t = Template(open(filename, 'rU').read())
    fout = open(filename, 'w')
    fout.write(t.render(context))
    fout.close

def submedia_files(topdir):
    """
    Runs ``subfile`` function on each media file
    from given directory.
    """
    settings_as_dict = get_settings_as_dict(settings)
    context = Context(settings_as_dict)
    for dir, subdirs, files in os.walk(topdir):
        filenames = [os.path.join(dir, file) for file in files]
        for file in filter(is_media_file, filenames):
            subfile(file, context)
    

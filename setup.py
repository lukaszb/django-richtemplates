from setuptools import setup, find_packages

richtemplates = __import__('richtemplates')
VERSION = richtemplates.__version__

def find_package_data():
    import os
    data_extensions = ['html', 'js', 'png', 'css', 'gif']
    data = {'richtemplates': []}
    topdir = 'richtemplates'
    for dir, subdirs, files in os.walk(topdir):
        for file in files:
            ext = file.split('.')[-1].lower()
            if ext in data_extensions:
                fpath = os.path.join(dir, file)[len('richtemplates/'):]
                data['richtemplates'].append(fpath)
    return data
import pprint

setup(
    name = 'django-richtemplates',
    version = VERSION,
    url = 'http://bitbucket.org/lukaszb/richtemplates/',
    author = 'Lukasz Balcerzak',
    author_email = 'lukasz.balcerzak@python-center.pl',
    description = 'Templates, media, tags for django based on Java Richfaces.',
    long_description = richtemplates.__doc__,
    packages = find_packages(),
    zip_safe = False,
    package_data = find_package_data(),
    scripts = [],
    requires = ['Djalog'],
    install_requires = [
        'djalog',
    ],
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
    ],
)


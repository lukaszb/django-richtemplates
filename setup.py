import sys
from setuptools import setup, find_packages

richtemplates = __import__('richtemplates')
VERSION = richtemplates.__version__
readme_file = 'README.rst'
try:
    long_description = open(readme_file).read()
except IOError, err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

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

setup(
    name = 'django-richtemplates',
    version = VERSION,
    url = 'http://bitbucket.org/lukaszb/django-richtemplates/',
    author = 'Lukasz Balcerzak',
    author_email = 'lukasz.balcerzak@python-center.pl',
    description = richtemplates.__doc__,
    long_description = long_description,
    packages = find_packages(),
    zip_safe = False,
    package_data = find_package_data(),
    scripts = [],
    requires = ['Djalog'],
    install_requires = [
        'Django>=1.2',
        'djalog',
        'django-annoying',
        'django-pagination>=1.0.7',
        'django-filter',
        'django-registration>=0.7',
        'django-native-tags',
        'docutils',
        'Pygments',
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


Installation
============

There are many ways to install python packages. Here I will list couple of
them.

Install the package
-------------------

You may install `richtemplates` either by downloading it from Cheese Shop
and install manually, cloning repository (hg clone
(`<http://bitbucket.org/lukaszb/richtemplates/>`_) or executing::

        easy_install richtemplates

with administrator priviliges. You may also download it and just put it at
your ``PYTHONPATH``.

Hook into your settings
-----------------------

Add `'richtemplates'` into your ``INSTALLED_APPS`` variable within
settings module.

Run::

        python manage.py richtemplates_init --media=media templates

This will copy initial templates structure and media files into your project.

Change your templates as you need.


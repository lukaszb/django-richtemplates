.. _installation:

Installation
============

``Richtemplates``, as most Python packages, can be installed in many ways,
including:

- :ref:`installation-automatic-package-manager`
- :ref:`installation-manual-pypi`
- :ref:`installation-manual-bitbucket`

Requirements
------------

``django-richtemplates`` needs `Django <http://www.djangoproject.com>`_ 1.2,
although it is possible to run it on version 1.1 too [1]_.

.. note::
   Despite it is not needed, if you intend to contribute on this project, or
   need to work on it at your fork, we suggest you installing `Djalog
   <http://pypi.python.org/pypi/Djalog/>`_ or simply configure logging module
   using ``logging.basicConfig`` method to be able to see logs during
   development.

.. _installation-automatic-package-manager:

Automatic installation using package manager
--------------------------------------------

Simply run::

    easy_install django-richtemplates

or::

    pip install django-richtemplates

.. _installation-manual-pypi:

Manual installation from source distribution
--------------------------------------------

Source archive of the most stable version is available at `Python Package
Index <http://pypi.python.org/pypi/django-richtemplates/>`_. Once you've
downloaded the archive, unpack it, go into newly created directory and type::

    python setup.py install

.. _installation-manual-bitbucket:

Manual installation from Mercurial repository
---------------------------------------------

Package is maintained at `bitbucket
<http://bitbucket.org/lukaszb/django-richtemplates/>`_ and if you'd like to
you may clone the repository using following command::

    hg clone http://bitbucket.org/lukaszb/django-richtemplates/

.. note::
   You'd need to have `Mercurial <http://www.selenic.com/mercurial/>`_
   installed on your system.

After you get clone of the repository, go into ``richtemplates`` directory
and run::

    python setup.py install

.. note::
   You will need superuser privileges in order to install the package.

.. [1] You need to provide ``django.contrib.messages`` for your Django
   installation and change some templates to work without CSRF security
   support.


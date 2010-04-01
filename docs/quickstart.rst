.. _quickstart:

Quickstart
==========

`django-richtemplates`_'s source distribution comes with example project
located at ``example_project`` of the archive. It's settings module is
configured so it would try to lookup `django-richtemplates`_ in it's parent
directory (so try not to move it).

Remember that `django-richtemplates`_ needs Django_ >=1.2 (see
:ref:`installation` and :ref:`configuration` sections for more information).

.. note::
   We strongly recommend to use virtualenv_, virtualenvwrapper_ and pip_
   combo. You could simply create virtual environment::

      mkvirtualenv --no-site-packages richtemplates_test

Simply follow those steps in order to get ``example_project`` running:

1. Go to the ``example_project`` directory
2. Install project's requirements: ``pip install -r requirements.txt``
3. Create sqlite database: ``python manage.py syncdb``
4. Import ``richtemplates`` and ``django-admin-tools`` media folders:
   ``python manage.py import_media richtemplates admin_tools``
5. Run development server ``python manage.py runserver``
6. Visit ``http://127.0.0.1:8000``

Example projects shows:

- Default `django-richtemplates`_ theme
- How messages are shown
- How to use ``base.html``, ``base_1col.html``, ``layout/menu_top.html``
  and many more templates
- How to use `django-pagination`_, `django-filter`_ and `django-sorting`_
  with `django-richtemplates`_.
- An example of how to use :ref:`limiting_model_form`
- An example of how to use :ref:`middleware-403`

.. _pip: http://pypi.python.org/pypi/pip
.. _django: http://www.djangoproject.com
.. _djalog: http://pypi.python.org/pypi/Djalog/
.. _django-pagination: http://code.google.com/p/django-pagination/
.. _django-sorting: http://github.com/directeur/django-sorting
.. _django-tables: http://bazaar.launchpad.net/~miracle2k/django-tables/trunk
.. _django-filter: http://github.com/alex/django-filter
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/

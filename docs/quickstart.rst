.. _quickstart:

Quickstart
==========

`django-richtemplates`_'s source distribution comes with example projet
located at ``example_project`` of the archive. It's settings module is
configured so it would try to lookup `django-richtemplates`_ in it's
parent directory (so try not to move it).

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
4. Import richtemplates media folder: ``python manage.py import_media
   richtemplates``
5. Run development server ``python manage.py runserver``
6. Visit ``http://127.0.0.1:8000``

.. _pip: http://pypi.python.org/pypi/pip
.. _django: http://www.djangoproject.com
.. _djalog: http://pypi.python.org/pypi/Djalog/
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/

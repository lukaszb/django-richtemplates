.. _example_project:

Example project
===============

`django-richtemplates`_'s source distribution comes with example projet
located at ``example_project`` of the archive. It's settings module is
configured so it would try to lookup `django-richtemplates`_ in it's
parent directory (so try not to move it).

Quickstart
==========

Remember that `django-richtemplates`_ needs Django_ >=1.2 (see
:ref:`installation` and :ref:`configuration` sections for more information).

.. note::
   Example project would try to use Djalog_ for better logging (sql + colored). 

Simply follow those steps in order to get ``example_project`` running:

1. Go to the ``example_project`` directory
2. Run ``python setup.py syncdb``
3. Run ``python manage.py import_media richtemplates``
4. Run ``python manage.py runserver`` and visit ``http://127.0.0.1:8000``


.. _django: http://www.djangoproject.com
.. _djalog: http://pypi.python.org/pypi/Djalog/
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/

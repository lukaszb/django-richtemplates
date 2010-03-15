.. _middleware:

==========
Middleware
==========

This section covers middleware classes available with `django-richtemplates`_.

.. _middleware-403:

HTTP 403 Middleware
-------------------

``Page does not exists`` (404 error code) has build in support in Django_ but
if it comes to the 403 error code handler it has nothing to offer *out-of-the
-box*. Well, in fact, it has, and it is crucial for this middleware's
implementation: ``django.http.HttpResponseForbidden``. If this middleware is
installed and instance of ``django.http.HttpResponseForbidden`` is returned
(which is done if ``django.core.exceptions.PermissionDenied`` is risen, too)
then ``403.html`` template is returned.

Installation
~~~~~~~~~~~~

In order to use ``Http403Middleware`` you have to add it to your
``MIDDLEWARE_CLASSES`` at settings module. Here is an example:

.. code-block:: python

   MIDDLEWARE_CLASSES = (
       'django.middleware.common.CommonMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.middleware.csrf.CsrfResponseMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.transaction.TransactionMiddleware',
   
       'richtemplates.middleware.Http403Middleware',
    )

.. note::
   Remember that 403 error code should be returned if server disallow user
   from entering a page so it is needed that this middleware comes
   *after* ``AuthenticationMiddleware`` most probably - it of course is
   up to you.

.. _django: http://www.djangoproject.com
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/

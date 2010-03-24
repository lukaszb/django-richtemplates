.. _userprofiles:

=============
User profiles
=============

At some point of building your project you may wish to allow users to store
some extra data. If you use Django_'s built-in authentication system you are
in luck - much of the code have been already written and you only have to:

1. Set up your profile's model class.
2. Point to the created model at your settings module.

If you are not familiar with Django_'s authentication framework, please refer
to Django_'s 
`documentation <http://docs.djangoproject.com/en/dev/topics/auth/>`_ on the
topic or.

Using richtemplate's user profile class
---------------------------------------

For convenience, ``richtemplates`` comes with basic ``UserProfile`` class. You
may use it directly by adding following line in your settings:

.. code-block:: python

   AUTH_PROFILE_MODULE = 'richtemplates.UserProfile'

Subclassing profile class
-------------------------

.. _django: http://www.djangoproject.com

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
topic.

Using richtemplate's user profile class
---------------------------------------

For convenience, ``richtemplates`` comes with basic ``UserProfile`` class. You
may use it directly by adding following line in your settings:

.. code-block:: python

   AUTH_PROFILE_MODULE = 'richtemplates.UserProfile'

This model provides only most basic fields:

* :py:attr:`user`: foreign key to :py:class:`django.contrib.auth.models.User`
* :py:attr:`skin`: defaults to :ref:`RICHTEMPLATES_DEFAULT_SKIN`, and should be
  a choice from :ref:`RICHTEMPLATES_SKINS`
* :py:attr:`code_style`: pygments style class sources should be pygmented with
  for the user

However, more probably you would like to extend this class - simply follow
guidelines described at :ref:`userprofiles-subclassing-profile-class`.

.. _userprofiles-subclassing-profile-class:

Subclassing profile class
-------------------------

If needed (well, most probably it is *needed* in one's project) ``UserProfile``
may be easy subclassed. Let's say we have main application where we define our
user profile model and *app label* is ``core``. We need to add address field at
profile model. Models code could look as follows::

    from django.db import models
    from richtemplates.models import UserProfile as RichUserProfile

    class UserProfile(RichUserProfile):
        address = models.CharField(max_length=128, null=True, blank=True)

Then, at settings file of our project we need to point at this class::

    AUTH_PROFILE_MODULE = 'core.UserProfile'

If we create pluggable application and want to make our user profile class
abstract until ``AUTH_PROFILE_MODULE`` is pointed at our model, we can add
simple check within :py:class:`Meta` class of our model::

    from django.conf import settings
    from django.db import models
    from richtemplates.models import UserProfile as RichUserProfile

    class UserProfile(RichUserProfile):
        
        address = models.CharField(max_length=128, null=True, blank=True)

        class Meta:
            abstract = getattr(settings, 'AUTH_PROFILE_MODULE', '') != \
                'core.UserProfile'
    

.. _django: http://www.djangoproject.com

.. _configuration:

=============
Configuration
=============

This section describes how to:

* `Hook richtemplates into your project`_
* `Import media files`_
* `Use optional components`_
* `Configure settings`_

Hook richtemplates into your project
====================================

This is done similar to other Django pluggable applications. Simply add
``richtemplates`` into your ``INSTALLED_APPS`` tuple at ``settings`` module.

Additionally, you need to add *context processor* provided by
``richtemplates`` at your ``settings`` module **AND** ``request`` *context
processor* which boundled with Django_ but not included by default:

.. code-block:: python

   from django.conf import global_settings
   
   # ...
   
   TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.request',
        'richtemplates.context_processors.media',
   )

This would allow to use ``{{ RICHTEMPLATES_MEDIA_URL }}`` context variable in templates
and it is necessary for ``richtemplates`` to work properly.



Import media files
==================

If you have already hooked ``richtemplates`` into your project you can use
*management command* in order to copy necessary media files. Simply run
following command:

.. code-block:: bash

   ./manage.py import_media richtemplates

Use optional components
=======================

TODO: Write about other richtemplates features.

Configure settings
==================

Following configuration settings may be overriden:

* `RICHTEMPLATES_MEDIA_URL`_
* `RICHTEMPLATES_SESSION_SKIN_NAME`_
* `RICHTEMPLATES_PROFILE_SKIN_FIELD`_
* `RICHTEMPLATES_DEFAULT_SKIN`_
* `RICHTEMPLATES_SKINS`_
* `RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES`_

.. _`RICHTEMPLATES_MEDIA_URL`:

``RICHTEMPLATES_MEDIA_URL``
    *Default*: same as ``django.conf.settings.MEDIA_URL + 'richtemplates/'``

    Used by *context processor* and provides ``RICHTEMPLATES_MEDIA_URL``
    context variable in templates.

.. _`RICHTEMPLATES_SESSION_SKIN_NAME`:

``RICHTEMPLATES_SESSION_SKIN_NAME``
    *Default*: ``'skin'``

    Used as key for skin field in sessions.
    
    See :ref:`skins` documentation.

.. _`RICHTEMPLATES_PROFILE_SKIN_FIELD`:

``RICHTEMPLATES_PROFILE_SKIN_FIELD``
    *Default*: ``'skin'``

    If you want to make users able to save information about their chosen
    skin you need to specify *field* name (on user profile model) on which
    that information would be stored/fetched.
    
    See :ref:`skins` documentation.

.. _`RICHTEMPLATES_DEFAULT_SKIN`:

``RICHTEMPLATES_DEFAULT_SKIN``
    *Default*: ``'aqua'``

    This is default skin alias for users who haven't already choose a skin
    they want to use.
    
    See :ref:`skins` documentation.

.. _`RICHTEMPLATES_SKINS`:

``RICHTEMPLATES_SKINS``
    *Default*:

    .. code-block:: python

       {
           'aqua': {'name': 'Aqua'},
           'django': {'name': 'Django'},
           'ruby': {'name': 'Ruby'},
       }

    If you want to extend exising skins with your own you would need to
    specify proper dictionary. You should see :ref:`skins` documentation.

.. _`RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES`:

``RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES``
    *Default*: ``{}``

    ``richtemplates`` comes with some support for restructuredText. It is still
    undocumented.

.. _Django: http://www.djangoproject.com


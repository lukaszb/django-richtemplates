.. django-richtemplates documentation master file, created by
   sphinx-quickstart on Fri Feb 19 00:30:57 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Richtemplates
=============

`django-richtemplates`_ is a set of templates (surprise!), template tags,
media files providing presentation layer similar to what Richfaces library
offers for J2EE developers - not outstanding but still nice looking and
elegant.

We wanted to have ability to prototype Django_ projects/applications
with some basic set of templates and thats why `django-richtemplates`_
was created. We use it for our company's intranet applications but it
can be also easily used for example projects in other Django_ pluggable
applications.

.. image:: _static/richtemplates-examples-home.png
   :width: 500px

Sources and issue tracker
~~~~~~~~~~~~~~~~~~~~~~~~~

Sources may be found at `bitbucket
<http://bitbucket.org/lukaszb/django-richtemplates/>`_. You may file a bug
there, too. 

License
~~~~~~~

`django-richtemplates`_ is an open source project released under MIT_ license.
Copy of the license should be boundled with source code archive.

Documentation
=============

**Installation and configuration topics:**

.. toctree::
   :maxdepth: 1
   
   quickstart
   installation
   configuration

**Richtemplates**

.. toctree::
   :maxdepth: 2

   forms
   middleware
   templates
   skins
   userprofiles

   api/index
..
   **Manual**
   
   .. toctree::
      :maxdepth: 1
   
      manual/index


**Included utilities:**

.. toctree::
   :maxdepth: 2

   management


Other topics
============

* :ref:`genindex`
* :ref:`search`

.. toctree::
   :maxdepth: 1
   :glob:

   screenshots
   documentation_guidelines

.. _django: http://www.djangoproject.com
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _mit: http://www.opensource.org/licenses/mit-license.php


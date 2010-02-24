.. _templates:

Templates
=========

This section covers information on `django-richtemplates`_'s templates.

Concepts and guidelines
-----------------------

There are some basic rules we try to stick with while building generic
templates. These are also guidelines for ourselves:

* Do not forget, `django-richtemplates`_ are builded for intranet
  applications, not public portals!
* We try to base on ``div`` tags rather than ``tables``
* While this is presentation layer supporting application we do include
  some basic code, like generic :ref:`forms` or :ref:`middleware`.
* We try to use names established by the community (for instance, our
  main template would be called ``base.html``)
* We use ``blocks`` inside previously prepared html tags.
  So this is ok:

  .. code-block:: django
  
     <body>
     {% block body %}
     ...
     {% endblock %}
     </body>

  And this is wrong:

  .. code-block:: django
  
     {% block body %}
     <body>
     ...
     </body>
     {% endblock %}

Moreover, we would use following few models as base for examples in this
document.

.. _templates-example-models:

Example models
~~~~~~~~~~~~~~

.. code-block:: python

   class Project(models.Model):
       name = models.CharField(max_length=32)
       is_public = models.BooleanField(default=True)
       created_at = models.DateTimeField(auto_now_add=True)
       created_by = models.ForeignKey(User)
   
   class Task(models.Model):
       summary = models.CharField(max_length=64)
       content = models.TextField()
       project = models.ForeignKey(Project)
       status = models.ForeignKey('Status')
       priority = models.ForeignKey('Priority')
       created_at = models.DateTimeField(auto_now_add=True)
       author = models.ForeignKey(User)
       edited_at = models.DateTimeField(auto_now=True)
       editor = models.ForeignKey(User)
   
   class Status(models.Model):
       name = models.CharField(max_length=16)
       project = models.ForeignKey(Project)
   
   class Priority(models.Model):
       name = models.CharField(max_length=16)
       project = models.ForeignKey(Project)

Layout
------

We will discuss main templates ``bases`` and their ``blocks`` here.

Top menus
~~~~~~~~~

Tables
~~~~~~

Generally we use one table layout to present data. We
decided not to use ``templatetags`` (provided by, for instance, django-tables_)
as in many situations we would like to have more flexible way to change
the looks & feel of the table. This may still change in future
as it seems is the *right* way.

After a few words of introduction here is an example of how you can use
provided set of styles in your template (we assume that ``task_list``
queryset is passed into the context and it is a queryset
of model ``Task`` defined at :ref:`templates-example-models` above):

.. code-block:: django 

   <table class="datatable">
       <thead class="datatable-thead">
           <tr class="datatable-thead-subheader">
               <th>ID</th>
               <th>Summary</th>
               <th>Created at</th>
               <th>Reported by</th>
               <th>Modified at</th>
               <th>Last editor</th>
               <th>Status</th>
           </tr>
       </thead>
       <tbody class="datatable-tbody">
           {% for task in task_list %}
           <tr class="{% cycle "odd" "even" %} hoverable">
               <td>{{ task.id }}</td>
               <td>{{ task.summary }}</td>
               <td>{{ task.created_at }}</td>
               <td>{{ task.author }}</td>
               <td>{{ task.edited_at }}</td>
               <td>{{ task.editor }}</td>
               <td>{{ task.status }}</td>
           </tr>
           {% endfor %}
       </tbody>
   </table>

Paginated tables
~~~~~~~~~~~~~~~~

In order to use django-pagination_ (which we do all the time) before we present
our table we need to:

1. Load django-pagination_ templatetags:

   .. code-block:: django

      {% load pagination_tags %}

2. Paginate given queryset:

   .. code-block:: django

      {% autopaginate task_list %}

3. And finally add ``paginate`` templatetag, below or on top of a table
   (or both):

   .. code-block:: django

      {% paginate %}

Sorted tables
~~~~~~~~~~~~~

In order to use django-sorting_ (which, again, we all do :)) before we present
our table we need to:

1. Load django-sorting_ templatetags:

   .. code-block:: django

      {% load sorting_tags %}

2. Sort given queryset:

   .. code-block:: django

      {% autosort task_list %}

3. And finally, use ``anchor`` templatetag to specify table headers:

   .. code-block:: django

      <td>{% anchor id "ID" %}</td>
      <td>{% anchor summary "Summary" %}</td>
      <td>{% anchor created_at "Created at" %}</td>
      <td>{% anchor author "Author" %}</td>
      <td>{% anchor edited_at "Modified at" %}</td>
      <td>{% anchor editor "Last editor" %}</td>
      <td>{% anchor status "Status" %}</td>

Sorted and paginated tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. _django: http://www.djangoproject.com
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _django-pagination: http://code.google.com/p/django-pagination/
.. _django-sorting: http://github.com/directeur/django-sorting
.. _django-tables: http://bazaar.launchpad.net/~miracle2k/django-tables/trunk

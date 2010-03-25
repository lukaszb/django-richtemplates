.. _templates:

Templates
=========

This section covers information on `django-richtemplates`_'s templates.

Concepts and guidelines
-----------------------

There are some basic rules we try to stick with while building generic
templates. These are also guidelines for ourselves:

* Do not forget, `django-richtemplates`_ are builded to simplify process of
  writing boilerplate codes at presentation layer but is not intended to make
  whole job for you
* We try to base on ``div`` tags rather than ``tables``
* While this is presentation layer supporting application we do include some
  basic code, like generic :ref:`forms` or :ref:`middleware`.
* We try to use names established by the community (for instance, our main
  template would be called ``base.html``)
* We use ``blocks`` inside previously prepared html tags.  So this is ok:

  .. code-block:: html+django
  
     <body>
     {% block body %}
     ...
     {% endblock %}
     </body>

  And this is wrong:

  .. code-block:: html+django
  
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

   import datetime
   from django.db import models
   from django.contrib.auth.models import User
   
   class Project(models.Model):
       name = models.CharField(max_length=32)
       is_public = models.BooleanField(default=True)
       created_at = models.DateTimeField(auto_now_add=True)
       created_by = models.ForeignKey(User)
   
       def __unicode__(self):
           return self.name
   
       @models.permalink
       def get_absolute_url(self):
           return ('richtemplates_examples_project_detail', (),
               {'project_id': self.id})
   
       @models.permalink
       def get_task_list_url(self):
           return ('richtemplates_examples_project_task_list', (),
               {'project_id': self.id})
   
   class Task(models.Model):
       summary = models.CharField(max_length=64)
       content = models.TextField(help_text="Uses restructuredText")
       project = models.ForeignKey(Project)
       status = models.ForeignKey('Status')
       priority = models.ForeignKey('Priority')
       created_at = models.DateTimeField(auto_now_add=True)
       author = models.ForeignKey(User, related_name='created_tasks')
       edited_at = models.DateTimeField(auto_now=True)
       editor = models.ForeignKey(User, related_name='edited_tasks')
   
       def __unicode__(self):
           return u'#%s %s' % (self.id, self.summary)
   
       @models.permalink
       def get_absolute_url(self):
           return ('richtemplates_examples_task_detail', (),
               {'task_id': self.id})
   
       @models.permalink
       def get_edit_url(self):
           return ('richtemplates_examples_task_edit', (),
               {'task_id': self.id})
   
       def get_duration(self):
           """
           Returns how long task is opened. If it is already
           resolved, time since creation till last edit is
           returned.
           """
           if self.status.is_resolved:
               return self.edited_at - self.created_at
           else:
               return datetime.datetime.now() - self.created_at
   
   
   class Status(models.Model):
       name = models.CharField(max_length=16)
       project = models.ForeignKey(Project)
       is_resolved = models.BooleanField(default=False)
   
       def __unicode__(self):
           return self.name    
   
       class Meta:
           verbose_name_plural = 'Statuses'
   
   class Priority(models.Model):
       name = models.CharField(max_length=16)
       project = models.ForeignKey(Project)
   
       def __unicode__(self):
           return self.name
   
       class Meta:
           verbose_name_plural = 'Priorities'
   
   
Layout
------

We will discuss main templates ``bases`` and their ``blocks`` here.

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

.. code-block:: html+django 

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

   .. code-block:: html+django

      {% load pagination_tags %}

2. Paginate given queryset:

   .. code-block:: html+django

      {% autopaginate task_list %}

3. And finally add ``paginate`` templatetag, below or on top of a table
   (or both):

   .. code-block:: html+django

      {% paginate %}

Sorted tables
~~~~~~~~~~~~~

In order to use django-sorting_ (which, again, we all do :)) before we present
our table we need to:

1. Load django-sorting_ templatetags:

   .. code-block:: html+django

      {% load sorting_tags %}

2. Sort given queryset:

   .. code-block:: html+django

      {% autosort task_list %}

3. And finally, use ``anchor`` templatetag to specify table headers:

   .. code-block:: html+django

      <th>{% anchor id "ID" %}</th>
      <th>{% anchor summary "Summary" %}</th>
      <th>{% anchor created_at "Created at" %}</th>
      <th>{% anchor author "Author" %}</th>
      <th>{% anchor edited_at "Modified at" %}</th>
      <th>{% anchor editor "Last editor" %}</th>
      <th>{% anchor status "Status" %}</th>


Forms
~~~~~


Simple example:

.. code-block:: html+django

   <form action="." method="post">
       <table class="form-table">
           {% include "richtemplates/forms/form.html" %}
       </table>
       <div>
           <input id="id_submit" type="submit" name="submit" value="Submit" />
       </div>
   </form>

.. _django: http://www.djangoproject.com
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _django-pagination: http://code.google.com/p/django-pagination/
.. _django-sorting: http://github.com/directeur/django-sorting
.. _django-tables: http://bazaar.launchpad.net/~miracle2k/django-tables/trunk


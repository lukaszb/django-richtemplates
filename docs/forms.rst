.. _forms:

=====
Forms
=====

`django-richtemplates`_ comes with some custom forms which are designed to be
reusable and easily extensible. Here is a list of available forms:

* :ref:`limiting_model_form`

.. _limiting_model_form:

LimitingModelForm
-----------------

This form allow us to choose a field on which other fields within same form
would rely on when it comes to make a query.

Example
~~~~~~~

Concept of this form is simple but let us start with some basics. Let's assume
we have one model which is *heart* of our scheme, and we have also 3 other
models which are related to the first one:

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

Our object here is to create a form for the ``Task``. We defined foreign key to
the project table as we want to be able to specify other statuses and
priorities for different projects. Normally we would create a form like this:

.. code-block:: python

   class TaskForm(forms.ModelForm):
       class Meta:
           model = Task

But with this approach our form would give us ability to choose status and
priority from all possible objects, related to each project. So we need to
override ``status`` and ``priority`` fields or create some factory method which
would return us a TaskForm with ``status`` and ``priority`` fields limited to
the previously chosen ``project``. And what if we would have to make more such
form classes? We do not want to break DRY rule, are we?  Sure we don't and
``LimitingModelForm`` is here for us! To make one we would simply add
``choices_limiting_fields`` option to our form's ``Meta`` subclass:

.. code-block:: python

   from richtemplates.forms import LimitingModelForm
   
   class TaskForm(LimitingModelForm):
       class Meta:
           choices_limiting_fields = ['project']

``LimitingModelForm`` directly extends ``django.forms.ModelForm`` class and at
the time of initialization, after normal ``django.forms.ModelForm.__init__``
logic it simply calls a method which limits already created fields with foreign
key to the model we specify in ``choices_limiting_fields`` iterable.

.. note::
   This is still somewhat experimental and overall implementation should be
   improved.

.. note::
   Do not use this form in admin! It would work perfectly fine for existing
   ``Task`` objects but if you'd try to create new one from admin a
   ``LimitingModelFormError`` would be risen as ``LimitingModelForm`` requires
   that field specified in ``chocies_limiting_fields`` option is already set on
   the object. This should be fixed though.

.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/

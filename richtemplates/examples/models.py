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


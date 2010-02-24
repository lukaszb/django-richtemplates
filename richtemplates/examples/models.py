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

class Task(models.Model):
    summary = models.CharField(max_length=64)
    content = models.TextField()
    project = models.ForeignKey(Project)
    status = models.ForeignKey('Status')
    priority = models.ForeignKey('Priority')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='created_tasks')
    edited_at = models.DateTimeField(auto_now=True)
    editor = models.ForeignKey(User, related_name='edited_tasks')

    def __unicode__(self):
        return u'#%s %s' % (self.id, self.summary)

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


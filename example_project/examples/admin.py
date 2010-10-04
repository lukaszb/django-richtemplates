from django import forms
from django.contrib import admin

from examples.models import Task, Status, Project, Priority
from richtemplates.forms import RestructuredTextAreaField


class TaskFormAdmin(forms.ModelForm):
    content = RestructuredTextAreaField()

    class Meta:
        model = Task

class TaskAdmin(admin.ModelAdmin):
    list_displa = ['project', 'summary', 'created_at', 'author', 'edited_at',
        'editor', 'status', 'priority']
    list_filter = ['author', 'status', 'priority']
    date_hierarchy = 'created_at'
    save_on_top = True
    search_fields = ['summary', 'content']
    form = TaskFormAdmin

class StatusInline(admin.StackedInline):
    model = Status
    extra = 1

class PriorityInline(admin.StackedInline):
    model = Priority
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_displa = ['id', 'name', 'author']
    save_on_top = True
    search_fields = ['name']
    inlines = [StatusInline, PriorityInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Priority)

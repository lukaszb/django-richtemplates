from django.contrib import admin

from examples.models import Task, Status, Project, Priority
from richtemplates.forms import LimitingModelForm

class TaskAdmin(admin.ModelAdmin):
    list_displa = ['project', 'summary', 'created_at', 'author', 'edited_at',
        'editor', 'status', 'priority']
    list_filter = ['author', 'status', 'priority']
    date_hierarchy = 'created_at'
    save_on_top = True
    search_fields = ['summary', 'content']

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

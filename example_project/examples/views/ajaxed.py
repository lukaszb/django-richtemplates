from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.shortcuts import render_to_response

from examples.models import Task

def get_task_list_page(page=1):
    try:
        page = int(page)
    except:
        page = 1
    paginate_by = 10
    paginator = Paginator(Task.objects.all(), paginate_by)
    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def task_list_ajaxed(request, template_name='examples/ajax/task_list.html'):
    items = get_task_list_page(1)
    context = {
        'items': items,
    }
    return render_to_response(template_name, context, RequestContext(request))

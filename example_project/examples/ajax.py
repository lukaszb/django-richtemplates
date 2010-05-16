from django.template.loader import render_to_string
from dajax.core import Dajax

from examples.views.ajaxed import get_task_list_page

def task_list_paginator(request, p):
    items = get_task_list_page(p)
    render = render_to_string('examples/ajax/task_list_page.html',
        {'items': items})

    dajax = Dajax()
    dajax.assign('#task-list-page', 'innerHTML', render)

    return dajax.json()



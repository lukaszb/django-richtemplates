# encoding: UTF-8
from django import template
from django.utils.html import escape

register = template.Library()

SEPARATOR = '/ '

class BreadCrumb(object):

    def __init__(self, name, url=None):
        self.name = escape(name)
        self.url = escape(url)

    def __repr__(self):
        return '<BreadCrumb "%s" with url="%s">' % (self.name, self.url)


class BreadCrumber(object):

    def __init__(self, path, start_from, trailing_slash=True,
                 separator='&rsaquo; ', domain_name=''):

        self.separator = separator
        self.domain_name = domain_name
        self.breadcrumbs = []

        # Remove protocol if in path
        if path.find('://')>0:
            path = path[path.find('://')+3:]
        urls = filter(lambda obj: obj, path.split('/')) # Removes if empty

        current_url = domain_name.rstrip('/') + '/'

        for i, url in enumerate(urls[:-1]):
            current_url += url
            if trailing_slash:
                current_url += '/'
            if i >= start_from:
                breadcrumb = BreadCrumb(url, current_url)
                self.breadcrumbs.append(breadcrumb)
            if not trailing_slash:
                # For next breadcrumb
                current_url += '/'

        if len(urls) > 0:
            # Last breadcrumb shouldn't be link
            url = urls[-1]
            breadcrumb = BreadCrumb(url)
            self.breadcrumbs.append(breadcrumb)


@register.inclusion_tag('richtemplates/extras/breadcrumbs.html')
def path_breadcrumbs(path, start_from='0', separator=SEPARATOR,
        trailing_slash=False):
    start_from = int(start_from)
    breadcrumber = BreadCrumber(path, start_from, separator=separator,
                                trailing_slash=trailing_slash)
    breadcrumbs = breadcrumber.breadcrumbs
    return {
        'breadcrumbs' : breadcrumbs,
        'separator' : separator,
    }


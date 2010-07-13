from django.test import TestCase
from django.template import Template, Context
from django.utils.html import escape

from richtemplates.templatetags.breadcrumber import SEPARATOR

def render(template, context={}):
    """
    Returns rendered ``template`` with ``context``, which are given as string
    and dict respectively.

    We always insert ``load breadcrumber`` at the beginning of template string.
    """
    template = '{% load breadcrumber %}' + template
    t = Template(template)
    return t.render(Context(context))

def render_stripped(template, context={}):
    """
    Same as ``render`` but would remove all \n and \t.
    """
    ret = render(template, context)
    return ret.replace('\n', '').replace('\t', '')

class BreadCrumberTest(TestCase):

    def _test_path(self, path, should_be, separator=SEPARATOR):
        ret = render_stripped('{% path_breadcrumbs path %}', {'path': path})
        self.assertTrue(ret == should_be, "Should return %s for path %s but "
            "got: %s" % (should_be, path, ret))

    def test_simple(self):
        for path in ('foo', 'foo/', '/foo', '/foo/'):
            self._test_path(path, 'foo')


        path = '/foo/bar/'
        self._test_path(path, '<a href="/foo">foo</a>/ bar')

        path = '/foo/bar/baz'
        self._test_path(path, ''.join((
            '<a href="/foo">foo</a>/ ',
            '<a href="/foo/bar">bar</a>/ ',
            'baz',
        )))

    def test_escape(self):
        path = '<script>alert(1)</script>'
        self._test_path(path, ''.join((
            '<a href="/%s">%s</a>/ ' % (escape('<script>alert(1)<'),
                escape('<script>alert(1)<')),
            escape('script>'),
        )))


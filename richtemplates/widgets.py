"""
Richtemplates provides some widgets helping to use it's styles and other
goodies.
"""
import string

from django import forms
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from richtemplates.templatetags.native import richicon_src
from richtemplates import settings as richtemplates_settings

from itertools import chain

class RichCheckboxSelectMultiple(forms.SelectMultiple):
    """
    Copied from django.forms.CheckboxSelectMultiple with additional img icons
    tags.  With javascript enabled allows to check single box by clicking on
    it's row / label / box. Uses nice css highlighting.

    Full example::

        from django import forms
        from richtemplates.widgets import RichCheckboxSelectMultiple
        def unslugify(value):
            return value.replace('_', ' ').replace('-', ' ').capitalize()

        class MultipleChoicesForm(forms.Form):
            CHOICES = ((key, unslugify(key)) for key in (
                ('view_project'),
                ('edit_project'),
                ('add_project'),
                ('delete_project'),
            ))
            fake_permissions = forms.MultipleChoiceField(choices=CHOICES,
                initial = ['view_project'],
                required = False,
                widget = RichCheckboxSelectMultiple)

    """

    class Media:
        js = (richtemplates_settings.MEDIA_URL +
            'js/jquery-richcheckboxselectmultiple.js',)

    def __init__(self, extra=True, *args, **kwargs):
        self.extra = extra
        super(RichCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        import logging
        logging.debug("Adding media %s" % RichCheckboxSelectMultiple.Media.js)
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        checkbox_class = 'richtable-checkbox'
        if attrs and 'class' in attrs:
            attrs['class'] = attrs['class'] + ' ' + checkbox_class
        else:
            attrs['class'] = checkbox_class
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<table class="datatable richcheckboxselectmultiple%s">' %
                    (attrs and 'class' in attrs and ' ' + attrs['class']),
                  u'<thead class="datatable-thead">',
                  u'<tr class="datatable-thead-subheader">'
                      u'<th>%s</th>' % _("State"),
                      u'<th>%s</th>' % _("Name"),
                      u'<th>%s</th>' % _("On/Off"),
                  u'</tr>',
                  u'</thead>',
                  ]
        if self.extra:
            output.append(
                u'<tfoot>'
                u'<tr><td colspan="3">'
                u'<a class="richbutton select-all">Select all</a>'
                u'<a class="richbutton deselect-all">Deselect all</a>'
                u'<a class="richbutton change-all">Reverse all</a>'
                u'</td></tr>'
                u'</tfoot>')

        output.append(u'<tbody class="datatable-tbody">')
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''
            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            # Adding img next to the field itself
            if option_value in str_values:
                src = richicon_src("icon-yes.gif")
            else:
                src = richicon_src("icon-no.gif")
            tr_class = i % 2 and "even" or "odd"
            img_tag = u'<img src="%s" alt="%s" />' % (src, src)
            output.append(u'<tr class="%s">'
                          u'<td class="centered">%s</td>'
                          u'<td><label%s>%s</label></td>'
                          u'<td>%s</td>'
                          u'</tr>' % (tr_class, img_tag, label_for,
                              option_label, rendered_cb))
        output.append(u'</tbody></table>')
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)


class RestructuredTextareaWidget(forms.Textarea):
    """
    Widget adding some extras from markItUp. Not using django-markitup as we
    needed only restructuredtext markup and by requiring to set that specific
    *filter* wouldn't allow one to use django-markitup with other renderer type.
    Ajax preview is nicer but it consumes more resources as it is called each
    time user hits keyboard - so use it on own risk.
    """

    def __init__(self, attrs=None, preview=True, preview_url=None):
        self.preview = preview
        self.preview_url = preview_url
        super(RestructuredTextareaWidget, self).__init__(attrs)

    class Media:
        js = (
            richtemplates_settings.MEDIA_URL + 'markitup/jquery.markitup.js',
            richtemplates_settings.MEDIA_URL +
                'markitup/sets/restructuredtext/set.js',
        )
        css = {
            'screen': (
                richtemplates_settings.MEDIA_URL +
                    'markitup/sets/restructuredtext/style.css',
                richtemplates_settings.MEDIA_URL +
                    'markitup/skins/richtemplates/style.css',
            ),
        }

    def render(self, name, value, attrs=None):
        html = super(RestructuredTextareaWidget, self).render(name, value, attrs)

        field_id = attrs['id']
        preview_id = field_id + '_preview'
        preview_title_id = preview_id + '_title'

        output = [
            '<h3 id="${preview_title_id}" class="markItUp-preview" '
                'style="display:none;">Preview</h3>',
            '<div id="${preview_id}" class="richtemplates-rst" '
                'style="display:none;"></div>',
            '<script type="text/javascript">',
            '(function($) {',
            '  $(document).ready(function(){',
            '    $("#${preview_id}").show();',
            '    $("#${preview_title_id}").show();',
            '    var field = $("#${field_id}");',
            '    field.markItUp(mySettings);',
            '    field.live("keyup", function(){',
            '      $.ajax({',
            '        url: "${preview_url}",',
            '        type: "POST",',
            '        data: {data: field.val()},',
            '        success: function(data){',
            '          $("#${preview_id}").html(data);',
            '        }',
            '      });',
            '    });',
            '  });',
            '})(jQuery);',
            '</script>',
        ]
        html = html + string.Template('\n'.join(output)).safe_substitute(
            field_id=field_id,
            preview_id=preview_id,
            preview_title_id=preview_title_id,
            preview_url=self.get_preview_url(),
        )
        return mark_safe(html)

    def get_preview_url(self):
        """
        Returns default url for rst preview processing view.
        """
        if self.preview_url is None:
            return reverse('richtemplates_rst_preview')
        return self.preview_url


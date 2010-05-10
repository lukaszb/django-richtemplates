from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from richtemplates.templatetags.native import richicon_src

from itertools import chain

class RichCheckboxSelectMultiple(forms.SelectMultiple):
    """
    Copied from django.forms.CheckboxSelectMultiple with additional
    img icons tags.
    """
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<table class="datatable">',
                  u'<thead class="datatable-thead">',
                  u'<tr class="datatable-thead-subheader">'
                      u'<th>%s</th>' % _("State"),
                      u'<th>%s</th>' % _("Name"),
                      u'<th>%s</th>' % _("On/Off"),
                  u'</tr>',
                  u'</thead>',
                  u'<tbody class="datatable-tbody">',
                  ]
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
            img_tag = u'<img src="%s" />' % src
            output.append(u'<tr class="%s">'
                          u'<td class="centered">%s</td>'
                          u'<td><label%s>%s</label></td>'
                          u'<td>%s</td>'
                          u'</tr>' % (tr_class, img_tag, label_for, option_label, rendered_cb))
        output.append(u'</tbody></table>')
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)


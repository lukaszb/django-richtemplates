# encoding: UTF-8

from django import forms
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe
from django.template import Template, Context

import logging

class DynamicActionChoice(object):
    """
    Should be given action number, label, additional fields if any.
    """

    def __init__(self, action, label, fields = {}):
        self.action = action
        self.label = label
        self.fields = fields

def DynamicActionFormFactory(available_choices, selected = None):
    """
    Returns Form object with radio choices based on available_choices
    but only selected ones are initialized. If selected (as sequence of
    action numbers) is not given, will return all possibilities.
    
    Raises exception if there are two DynamicActionChoice with same
    'action' number within available_choices.
    
    Creates basic clean up mechanism - only fields of the chosen action
    radio button are passed to the cleaned_data, others are removed. As so,
    if extended, form should call super(*cls*, self).clean() method if
    overriden.
    """

    class SameActionChoiceError(Exception):
        pass 
    
    if (selected is None):
        enabled_choices = available_choices
    else:
        enabled_choices = [ choice for choice in available_choices if (choice.action in selected) ]
    
    fields = {
        'action_type' : forms.TypedChoiceField(
            choices=[ (choice.action, choice.label) for choice in enabled_choices ],
            initial=enabled_choices[0].action,
            widget=forms.RadioSelect,
            coerce=int),
    }

    for choice in enabled_choices:
        for (field_name, field,) in choice.fields.items():
            field.required = False
            fields[field_name] = field
            logging.debug(('setting required of field %s to False' % field_name))

    def clean(self):
        cleaned_data = self.cleaned_data
        chosen_action = cleaned_data['action_type']
        self.chosen_action = chosen_action
        logging.debug("Chosen action: %s" % chosen_action)
        for choice in enabled_choices:
            if (choice.action == chosen_action):
                for (field_name, field,) in choice.fields.items():
                    if (cleaned_data.get(field_name, None) is None) and \
                            not self._errors.has_key(field_name):
                        self._errors[field_name] = ErrorList(['This field is required'])
        return cleaned_data
    
    def as_p_rows(self):
        """
        Should return <p> tags with one action radio plus any associated fields,
        in a single row.
        """
        output = []

        dynchoices = {}
        data = {}
        context = Context(data)
        
        chosen_action = int( self.dynfields['action_type'].data or enabled_choices[0].action )
        
        for choice in enabled_choices:
            dynchoices[choice.action] = choice
            fields = []
            for name, field in choice.fields.items():
                for dynname, dynfield in self.dynfields.items():
                    if name == dynname:
                        fields.append(dynfield)
            data = {
                'action' : choice.action,
                'label' : choice.label,
                'fields' : fields, 
            }
            row = '<p><input type="radio" name="action_type" id="id_action_type_{{ action }}"'
            row += ' value="{{ action }}"'
            if chosen_action == choice.action:
                row += ' checked="checked"'
            row += '/>'
            row += '<label>{{ label }}</label>{% for field in fields %}{{ field }}'
            row += '{% for error in field.errors %}<span class="error">{{ error }}</span>{% endfor %}'
            row += '{% endfor %}</p>'
            t = Template(row)
            row_output = t.render(Context(data))
            output.append( row_output )

        return mark_safe('\n'.join(output))
    
    # Constructor of the newly created form class
    def __init__(self, *args, **kwargs):
        super( type(self), self).__init__(*args, **kwargs)
        self.dynfields = {}
        for field in self:
            self.dynfields[field.name] = field

    form = type('DynamicActionForm', (forms.BaseForm,),
            {
                '__init__': __init__,
                'base_fields': fields,
                'clean': clean,
                'as_p_rows': as_p_rows,
                'enabled_choices': enabled_choices,
            }
    )

    class Media:
        js = ('{{ MEDIA_URL }}richtemplates/js/action_form.js',)
    form.Media = Media
   
    return form


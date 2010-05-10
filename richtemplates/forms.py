# encoding: UTF-8

from django import forms
from django.db import models
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template import Template, Context

from richtemplates import settings as richtemplates_settings
from richtemplates.utils import get_fk_fields, get_user_profile_model
from richtemplates.skins import get_skins
from richtemplates.fields import RestructuredTextAreaField, UserByNameField,\
    ModelByNameField
from richtemplates.widgets import RichCheckboxSelectMultiple

__all__ = ['RestructuredTextAreaField', 'UserByNameField', 'ModelByNameField',
    'DynamicActionChoice', 'DynamicActionFormFactory', 'LimitingModelFormError',
    'LimitingModelForm', 'RichCheckboxSelectMultiple',]

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

    def clean(self):
        cleaned_data = self.cleaned_data
        chosen_action = cleaned_data.get('action_type')
        if chosen_action is None or chosen_action == u'':
            #logging.debug("Cleaned data:\n%s" % cleaned_data)
            raise forms.ValidationError(_("Choose one action first"))
        self.chosen_action = chosen_action
        #logging.debug("Chosen action: %s" % chosen_action)
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
        Context(data)

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

        return mark_safe(u'\n'.join(output))

    # Constructor of the newly created form class
    def __init__(self, *args, **kwargs):
        # allow instance parameter
        self.instance = kwargs.pop('instance', None)
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

    return form


# =================================== #
# Limiting choices ModelForm subclass #
# =================================== #

class LimitingModelFormError(Exception):
    pass

class LimitingModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LimitingModelForm, self).__init__(*args, **kwargs)
        self._meta.choices_limiting_models = self._get_limiting_model_fields()
        self._limit_querysets()

    def _get_limiting_model_fields(self):
        """
        Returns model's field instances that should limit querysets of
        other fields at this form.
        """
        limiting_field_names = getattr(self.Meta, 'choices_limiting_fields', [])
        limiting_fields, limiting_models = [], []
        for fieldname in limiting_field_names:
            field = self._meta.model._meta.get_field_by_name(fieldname)[0]
            if not isinstance(field, models.ForeignKey):
                raise LimitingModelFormError("Choices limiting field should "
                    "be an instance of django.db.models.ForeignKey")
            model = field.related.parent_model
            if model in limiting_models:
                raise LimitingModelFormError("Cannot limit choices using "
                    "foreign keyed model more than once. Crashed at field "
                    "'%s'" % (field.name))
            limiting_models.append(model)
            limiting_fields.append(field)

        return limiting_fields

    def _limit_querysets(self):
        """
        Limits querysets of the fields using
        self._meta.choices_limiting_fields.
        """

        for model_field in self._get_limiting_model_fields():
            limiting_model = model_field.related.parent_model
            for bfield in self:
                field = bfield.field
                if not isinstance(field, forms.ModelChoiceField):
                    continue

                model_to_check = field.queryset.model
                fk_fields = get_fk_fields(model_to_check, limiting_model)

                if len(fk_fields) > 1:
                    raise LimitingModelFormError("Too many fk'd fields")
                elif fk_fields and limiting_model is fk_fields[0].related.parent_model:
                    try:
                        limit_to = getattr(self.instance, model_field.name)
                        field.queryset = field.queryset\
                            .filter(**{model_field.name: limit_to})
                    except limiting_model.DoesNotExist:
                        raise LimitingModelFormError("Tried to limit field "
                            "'%s' but it's instance field is empty"
                            % model_field.name)


# =================================== #
# Richtemplates user profiles helpers #
# =================================== #

class RichSkinChoiceField(forms.ChoiceField):
    """
    Use this field for a user profile form if you want to allow users to
    set their default skin.
    """
    def __init__(self, *args, **kwargs):
        super(RichSkinChoiceField, self).__init__(*args, **kwargs)
        self.choices = [(skin.alias, skin.name) for skin in get_skins()]

class RichCodeStyleChoiceField(forms.ChoiceField):
    """
    Use this field for user profile form if you want to allow users to set
    their code style used by pygments to highlight code snipppets.
    """
    def __init__(self, *args, **kwargs):
        super(RichCodeStyleChoiceField, self).__init__(*args, **kwargs)
        self.choices = [(alias, alias.title()) for alias in
            sorted(richtemplates_settings.REGISTERED_PYGMENTS_STYLES.keys())]

class UserProfileForm(forms.ModelForm):
    skin = RichSkinChoiceField()
    code_style = RichCodeStyleChoiceField()

    class Meta:
        exclude = ('user',)
        model = get_user_profile_model()


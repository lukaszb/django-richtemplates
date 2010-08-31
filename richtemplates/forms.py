# encoding: UTF-8

from django import forms
from django.db import models

from richtemplates import settings as richtemplates_settings
from richtemplates.utils import get_fk_fields, get_user_profile_model
from richtemplates.skins import get_skins
from richtemplates.fields import RestructuredTextAreaField, UserByNameField,\
    ModelByNameField
from richtemplates.widgets import RichCheckboxSelectMultiple

__all__ = ['RestructuredTextAreaField', 'UserByNameField', 'ModelByNameField',
    'LimitingModelFormError', 'LimitingModelForm', 'RichCheckboxSelectMultiple']

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


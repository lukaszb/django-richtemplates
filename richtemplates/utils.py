import logging

from django import forms
from django.db import models
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _

def has_rel_to_model(form_field, model):
    """
    Returns True if given form field is instance of
    ModelChoiceField and its queryset can be limited
    to the given model's instance (which means if this
    queryset's model has ForeignKey field to a given
    model this function will return True).
    Given form field should be instance of django.forms.Field.
    """
    if not isinstance(form_field, forms.ModelChoiceField):
        return False
    field_model = form_field.queryset.model
    for field in field_model._meta.fields:
        if isinstance(field, models.ForeignKey) and \
            field.related.parent_model is model:
            return True
    return False

def get_fk_fields(model, rel_model):
    """
    Searches for ForeignKey field in a given model
    with relation to rel_model.
    """
    related_fields = []
    for field in model._meta.fields:
        if isinstance(field, models.ForeignKey) and \
            field.related.parent_model is rel_model:
                related_fields.append(field)
    return related_fields

def get_skin_for_request(request):
    """
    Returns skin *alias* for the given request.
    """
    from richtemplates import settings as richtemplates_settings
    if hasattr(request, 'user') and request.user.is_authenticated():
        profile = request.user.get_profile()
        if profile and hasattr(profile, richtemplates_settings.PROFILE_SKIN_FIELD):
            skin_alias = getattr(profile, richtemplates_settings.PROFILE_SKIN_FIELD)
            if skin_alias not in richtemplates_settings.SKINS.keys():
                messages.warn(request, _("You should check your skin setting "
                    "in profile"))
            return richtemplates_settings.SKINS[skin_alias]
        else:
            skin_alias = richtemplates_settings.DEFAULT_SKIN
    else:
        skin_alias = richtemplates_settings.DEFAULT_SKIN

    return richtemplates_settings.SKINS[richtemplates_settings.DEFAULT_SKIN]


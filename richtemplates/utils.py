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

def get_user_profile_model(settings_module=settings):
    """
    Returns class of user profiles or None if it is pointed at
    settings (with ``AUTH_PROFILE_MODULE`` variable) or is pointed
    wrongly (default ``get_model`` behaviour).
    """
    if not hasattr(settings, 'AUTH_PROFILE_MODULE'):
        return None
    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    model = models.get_model(app_label, model_name)
    return model


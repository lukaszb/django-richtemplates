from django import forms
from django.db import models

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


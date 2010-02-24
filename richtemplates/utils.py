import logging

from django import forms
from django.db import models
from django.conf import settings
from docutils.parsers.rst import directives

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

def register_rst_directives(directives_items):
    """
    Registers restructuredText directives given as dictionary
    with keys being names and paths to directive function.
    """
    for name, directive_path in directives_items:
        try:
            splitted = directive_path.split('.')
            mod_path, method_name = '.'.join(splitted[:-1]), splitted[-1]
            mod = __import__(mod_path, (), (), [method_name], -1)
            directive = getattr(mod, method_name)
            directives.register_directive(name, directive)
            msg = "Registered restructuredText directive: %s" % method_name
            logging.debug(msg)
        except ImportError, err:
            msg = "Couldn't register restructuredText directive. Original "\
                "exception was: %s" % err
            logging.warn(msg)


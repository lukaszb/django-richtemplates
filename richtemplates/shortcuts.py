from django.db import models
from django.shortcuts import _get_queryset

def get_first_or_None(klass, *args, **kwargs):
    """
    Similar to ``django.shortcuts.get_object_or_404`` but tries to fetch
    first item from the query and if it does *NOT* exist None is returned
    rather than raising exception.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset[0]
    except IndexError:
        return None
    

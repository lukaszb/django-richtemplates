import logging

from django.test import TestCase, Client
from django.db import models
from django.contrib.auth.models import User

from richtemplates.utils import get_user_profile_model, settings
from richtemplates.models import UserProfile

class UserProfileTests(TestCase):
    pass

class GetUserProfileModelTests(TestCase):
    
    AUTH_PROFILE_MODULE_COPY = getattr(settings, 'AUTH_PROFILE_MODULE_COPY',
        None)

    def test_empty_setting(self):
        """
        Tests user profile helpers when ``AUTH_PROFILE_MODULE`` is not defined.
        """
        if hasattr(settings, 'AUTH_PROFILE_MODULE'):
            delattr(settings, 'AUTH_PROFILE_MODULE')
        self.assertTrue(get_user_profile_model() is None)
        if self.AUTH_PROFILE_MODULE_COPY:
            settings.AUTH_PROFILE_MODULE = self.AUTH_PROFILE_MODULE_COPY
        self.assertTrue(UserProfile._meta.abstract is True)

    def test_basic(self):
        """
        Test user profile helpers normally.
        """
        if hasattr(settings, 'AUTH_PROFILE_MODULE'):
            self.assertTrue(get_user_profile_model() is not None, "Received "
                "user profile model is %s" % get_user_profile_model(settings))
            if settings.AUTH_PROFILE_MODULE != 'richtemplates.UserProfile':
                self.assertTrue(UserProfile._meta.abstract is True)
            else:
                self.assertTrue(UserProfile._meta.abstract is False)
        
        


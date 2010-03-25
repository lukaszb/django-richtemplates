import urlparse

from django.conf import settings
from django.test import TestCase, Client
from django.template.defaultfilters import slugify

import richtemplates.settings
from richtemplates.skins import RichSkin, WrongSkinAlias
from richtemplates.skins import get_skins
from richtemplates.skins import get_skin_by_alias
from richtemplates.skins import get_skin_from_request
from richtemplates.skins import set_skin_at_request

class RichSkinTests(TestCase):

    skins = [RichSkin(**skin_info) for skin_info in (
        dict(alias='foo'),
        dict(alias='foo', name='bar'),
        dict(alias='foo', name='bar', url='/path/to/media/baz.css'),
        dict(alias='foo', url='http://www/path/to/media/baz.css'),
    )]

    def test_alias(self):
        for skin in self.skins:
            self.assertTrue(hasattr(skin, 'alias'))
            self.assertTrue(skin.alias is not None)
            self.assertTrue(skin.alias == slugify(skin.alias))
        
        # Should raise WrongSkinAlias if given alias is not a slug
        self.failUnlessRaises(WrongSkinAlias, RichSkin, '#23')
        self.failUnlessRaises(WrongSkinAlias, RichSkin, None)

    def test_name(self):
        for skin in self.skins:
            self.assertTrue(hasattr(skin, 'name'))
            self.assertTrue(isinstance(skin.name, str))

    def test_url(self):
        for skin in self.skins:
            self.assertTrue(hasattr(skin, 'url'))
            self.assertTrue(skin.url is not None)
            self.assertTrue(isinstance(skin.url, str))

            parsed = urlparse.urlparse(skin.url)
            self.assertTrue(parsed.scheme and parsed.netloc or 
                parsed.path.startswith('/'))
            self.assertTrue(parsed.path.find('//') == -1)
    
    def test_skin_with_local_css(self):
        skin = RichSkin('foo')
        self.assertTrue(skin.url is not None)
        self.assertTrue(isinstance(skin.url, str))

        parsed = urlparse.urlparse(skin.url)
        self.assertTrue(parsed.path.find('//') == -1)
        self.assertTrue(parsed.path.startswith(settings.MEDIA_URL))
        self.assertTrue(parsed.path.startswith(richtemplates.settings.MEDIA_URL))


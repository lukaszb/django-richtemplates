from richtemplates import settings as richtemplates_settings

def media(request):
    return {'RICHTEMPLATES_MEDIA_URL': richtemplates_settings.MEDIA_URL }


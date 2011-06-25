from richtemplates import settings as richtemplates_settings

def media(request):
    return {
        'RICHTEMPLATES_STATIC_URL': richtemplates_settings.STATIC_URL,
    }


from django.utils import translation
from django.conf import settings

def language_middleware(get_response):
    def middleware(request):
        language = request.session.get('django_language', 'en')
        translation.activate(language)
        request.LANGUAGE_CODE = language
        response = get_response(request)
        return response
    return middleware

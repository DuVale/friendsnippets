from django.contrib.flatpages.views import flatpage
from django.http import Http404
from django.conf import settings

# the accept parser to run multiple times for one user.
_accepted = {}

def get_current_language(request):

    supported = dict(settings.LANGUAGES)
    if hasattr(request, 'session'):
        lang_code = request.session.get('django_language', None)
        if lang_code in supported and lang_code is not None:
            return lang_code
    lang_code = request.COOKIES.get('django_language', None)
    if lang_code in supported and lang_code is not None:
        return lang_code

    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', None)
    if accept is not None:

        t = _accepted.get(accept, None)
        if t is not None:
            return t

        def _parsed(el):
            p = el.find(';q=')
            if p >= 0:
                lang = el[:p].strip()
                order = int(float(el[p+3:].strip())*100)
            else:
                lang = el
                order = 100
            p = lang.find('-')
            if p >= 0:
                mainlang = lang[:p]
            else:
                mainlang = lang
            return (lang, mainlang, order)

        langs = [_parsed(el) for el in accept.split(',')]
        langs.sort(lambda a,b: -1*cmp(a[2], b[2]))

        for lang, mainlang, order in langs:
            if lang in supported or mainlang in supported:
                _accepted[accept] = lang
                return lang

    return settings.LANGUAGE_CODE

class i18nFlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        try:
            flatpage=flatpage(request, request.path)

        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response

import re

from django.contrib.auth.views import redirect_to_login
from django.conf import settings


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    # Source: https://stackoverflow.com/a/3238410
    # Ported to Django 2.0: https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(settings.LOGIN_URL.lstrip('/'))]
        if hasattr(settings, 'LOGIN_REQUIRED_EXEMPT_URLS'):
            self.exempt_urls += [re.compile(expr) for expr in settings.LOGIN_REQUIRED_EXEMPT_URLS]

    def __call__(self, request):
        if not hasattr(request, 'user'):
            raise Exception('LoginRequiredMiddleware: authentication middleware not running')
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in self.exempt_urls):
                return redirect_to_login(request.path)
        response = self.get_response(request)
        return response

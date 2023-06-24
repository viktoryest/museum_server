from django.utils.deprecation import MiddlewareMixin

from museum import settings


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        if settings.DEBUG:
            setattr(request, '_dont_enforce_csrf_checks', True)


class StaticFilesCachingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'static' in request.path:
            max_age = 60 * 60 * 24
            response['Cache-Control'] = f'public, max-age={max_age}'
        return response

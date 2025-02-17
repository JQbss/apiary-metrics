import base64

from django.conf import settings
from django.http import HttpResponse


class DocsBasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/docs/') or request.path.startswith('/api/schema'):
            if 'HTTP_AUTHORIZATION' not in request.META:
                return self.unauthorized_response()

            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) != 2 or auth[0].lower() != 'basic':
                return self.unauthorized_response()

            username, password = base64.b64decode(auth[1]).decode().split(':')
            if username != settings.DOCS_USERNAME or password != settings.DOCS_PASSWORD:
                return self.unauthorized_response()

        return self.get_response(request)

    def unauthorized_response(self):
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Apiary Metrics API"'
        return response

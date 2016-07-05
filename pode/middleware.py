from urllib.parse import urlparse
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.http import HttpResponseRedirect


SANDBOXED_VIEWS = []


def sandboxed_user_code(func):
    SANDBOXED_VIEWS.append(func)

    return func


def sandboxed_user_code_middleware(get_response):
    if not (settings.SANDBOXED_ORIGIN and settings.UNSANDBOXED_ORIGIN):
        raise MiddlewareNotUsed()

    sandboxed_host = urlparse(settings.SANDBOXED_ORIGIN).netloc
    unsandboxed_host = urlparse(settings.UNSANDBOXED_ORIGIN).netloc

    def middleware(request):
        response = get_response(request)

        host = request.META['HTTP_HOST']

        if request.resolver_match:
            if request.resolver_match.func in SANDBOXED_VIEWS:
                if host != sandboxed_host:
                    return HttpResponseRedirect(settings.SANDBOXED_ORIGIN +
                                                request.path)
            else:
                if host != unsandboxed_host:
                    return HttpResponseRedirect(settings.UNSANDBOXED_ORIGIN +
                                                request.path)

        return response

    return middleware

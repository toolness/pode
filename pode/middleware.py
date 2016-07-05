from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.http import HttpResponseRedirect


SANDBOXED_VIEWS = []


def sandboxed_user_code(func):
    '''
    Marks the given view function as returning untrusted user-generated
    code that should be delivered on a separate origin (i.e., "sandboxed").
    '''

    SANDBOXED_VIEWS.append(func)

    return func


def get_request_origin(request):
    '''
    Return the origin of the given request, e.g. `https://foo.com`.
    '''

    return request.build_absolute_uri('/')[:-1]


def sandboxed_user_code_middleware(get_response):
    '''
    Middleware to ensure that untrusted user-generated code is always
    delivered on a separate origin from the rest of the application.
    '''

    if not (settings.SANDBOXED_ORIGIN and settings.UNSANDBOXED_ORIGIN):
        raise MiddlewareNotUsed()

    def middleware(request):
        response = get_response(request)

        request_origin = get_request_origin(request)

        if request.resolver_match:
            if request.resolver_match.func in SANDBOXED_VIEWS:
                if request_origin != settings.SANDBOXED_ORIGIN:
                    return HttpResponseRedirect(settings.SANDBOXED_ORIGIN +
                                                request.path)
            else:
                if request_origin != settings.UNSANDBOXED_ORIGIN:
                    return HttpResponseRedirect(settings.UNSANDBOXED_ORIGIN +
                                                request.path)

        return response

    return middleware

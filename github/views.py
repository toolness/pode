from urllib.parse import urlencode
import django.contrib.auth
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url


GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_SCOPES = []


def login_error(request, error_code):
    # TODO: Use a template. Be friendly.
    return HttpResponse('ERROR: %s' % error_code)


def login(request):
    request.session['oauth2_next_url'] = request.GET.get('next', '')
    request.session['oauth2_state'] = get_random_string(length=32)
    callback_url = request.build_absolute_uri(reverse('github:callback'))
    url = GITHUB_AUTH_URL + '?' + urlencode({
        'client_id': settings.GITHUB_CLIENT_ID,
        'redirect_uri': callback_url,
        'scope': ' '.join(GITHUB_SCOPES),
        'state': request.session['oauth2_state'],
    })
    return HttpResponseRedirect(url)


def callback(request):
    code = request.GET.get('code')
    expected_state = request.session.get('oauth2_state')
    state = request.GET.get('state')

    if state is None:
        return login_error(request, 'missing_state')

    if expected_state is None:
        return login_error(request, 'missing_session_state')

    if state != expected_state:
        return login_error(request, 'invalid_state')

    if code is None:
        return login_error(request, 'missing_code')

    user = django.contrib.auth.authenticate(github_oauth2_code=code,
                                            request=request)

    if user is None:
        return login_error(request, 'invalid_code_or_nonexistent_user')

    del request.session['oauth2_state']

    django.contrib.auth.login(request, user)

    next_url = request.session['oauth2_next_url']
    del request.session['oauth2_next_url']

    if not is_safe_url(url=next_url, host=request.get_host()):
        next_url = resolve_url(settings.LOGIN_REDIRECT_URL)

    return HttpResponseRedirect(next_url)

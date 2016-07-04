import logging
from django.conf import settings
from django.contrib.auth.models import User
import requests


USER_AGENT = 'Pode-App'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_URL = 'https://api.github.com/user'

logger = logging.getLogger(__name__)


def get_or_create_user(username, email):
    users = User.objects.filter(username=username)
    if len(users) == 0:
        user = User.objects.create_user(username, email)
        return user
    else:
        return users[0]


def exchange_code_for_access_token(code):
    payload = {
        'code': code,
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET
    }

    token_req = requests.post(GITHUB_TOKEN_URL, data=payload, headers={
        'User-Agent': USER_AGENT,
        'Accept': 'application/json'
    })
    if token_req.status_code != 200:
        logger.warn('POST %s returned %s '
                    'w/ content %s' % (
                        GITHUB_TOKEN_URL,
                        token_req.status_code,
                        repr(token_req.content)
                    ))
        return None

    response = token_req.json()
    return response['access_token']


def get_user_info(access_token):
    user_req = requests.get(GITHUB_USER_URL, headers={
        'User-Agent': USER_AGENT,
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token %s' % access_token
    })
    if user_req.status_code != 200:
        logger.warn('GET %s returned %s '
                    'w/ content %s' % (
                        GITHUB_USER_URL,
                        user_req.status_code,
                        repr(user_req.content)
                    ))
        return None

    return user_req.json()


class GithubBackend:
    def authenticate(self, github_oauth2_code=None, **kwargs):
        if github_oauth2_code is None:
            return None

        access_token = exchange_code_for_access_token(github_oauth2_code)
        if access_token is None:
            return None

        user_info = get_user_info(access_token)
        if user_info is None:
            return None

        # TODO: It's possible for email to be null because it's the
        # user's publicly visible email address, and they may have
        # opted-out of showing one publicly.

        user = get_or_create_user(user_info['login'], user_info['email'])
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

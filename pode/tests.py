from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from .models import UserCode
from . import middleware


class ModelTests(TestCase):
    def test_create_from_title_works(self):
        user = User.objects.create_user(username='foo')
        code = UserCode.objects.create_from_title(user, 'Boop')
        self.assertEqual(code.slug, 'boop')
        self.assertEqual(code.owner, user)

        code2 = UserCode.objects.create_from_title(user, 'Boop')
        self.assertEqual(code2.slug, 'boop-2')


class MiddlewareTests(TestCase):
    def test_get_request_origin_works(self):
        factory = RequestFactory()
        request = factory.get('/foo/bar/')
        self.assertEqual(middleware.get_request_origin(request),
                         'http://testserver')


class ViewTests(TestCase):
    def test_home_has_login_link_when_logged_out(self):
        res = self.client.get('/')
        self.assertContains(res, 'Login via GitHub')
        self.assertEqual(res.status_code, 200)

    def test_home_has_logout_link_when_logged_in(self):
        user = User.objects.create_user(username='foo')
        self.client.force_login(user)
        res = self.client.get('/')
        self.assertContains(res, 'Logout foo')
        self.assertEqual(res.status_code, 200)

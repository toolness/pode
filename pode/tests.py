from django.contrib.auth.models import User
from django.test import TestCase


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

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.urls import reverse

from portal.models import Environment
from django.test.client import RequestFactory


class EnvironmentTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_set_environment_into_session(self):
        environment_name = 'Campinas'
        request = self.factory.post(reverse('set_environment'))

        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        environment = Environment(name=environment_name)
        environment.set_environment_into_session(request)
        self.assertEqual(request.session['environment'], environment_name)

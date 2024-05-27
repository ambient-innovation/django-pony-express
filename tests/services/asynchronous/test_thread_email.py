from threading import Thread
from unittest import mock

from django.test import TestCase

from django_pony_express.services.asynchronous.thread import ThreadEmailService


class ThreadEmailServiceTest(TestCase):
    @mock.patch.object(Thread, "start")
    def test_process_regular(self, mocked_start):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = ThreadEmailService(recipient_email_list=[email])
        service.subject = subject
        service.template_name = "testapp/test_email.html"

        self.assertIsNone(service.process())
        mocked_start.assert_called_once()

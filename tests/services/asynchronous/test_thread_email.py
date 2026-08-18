import threading
from smtplib import SMTPServerDisconnected
from threading import Thread
from unittest import mock

from django.core import mail
from django.test import TestCase

from django_pony_express.services.asynchronous.thread import ThreadEmailService

BROKEN_EMAIL_BACKEND = "testapp.mail_backends.BrokenEmailBackend"


class ThreadEmailServiceTest(TestCase):
    @staticmethod
    def _build_service(**kwargs) -> ThreadEmailService:
        service = ThreadEmailService(recipient_email_list=["albertus.magnus@example.com"], **kwargs)
        service.subject = "Test email"
        service.template_name = "testapp/test_email.html"
        return service

    @mock.patch.object(Thread, "start")
    def test_process_regular(self, mocked_start):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = ThreadEmailService(recipient_email_list=[email])
        service.subject = subject
        service.template_name = "testapp/test_email.html"

        self.assertIs(service.process(), True)
        mocked_start.assert_called_once()

    @mock.patch.object(Thread, "start")
    @mock.patch.object(ThreadEmailService, "is_valid", return_value=False)
    def test_process_invalid(self, mocked_service, mocked_start):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = ThreadEmailService(recipient_email_list=[email])
        service.subject = subject
        service.template_name = "testapp/test_email.html"

        self.assertIs(service.process(), False)
        mocked_start.assert_not_called()

    def test_process_reports_errors_via_excepthook(self):
        """
        The error can't reach `process()`, but it must leave `_send_and_log_email()` so that it ends up in
        `threading.excepthook` and therefore in the error monitoring.
        """
        service = self._build_service(connection=mail.get_connection(backend=BROKEN_EMAIL_BACKEND))
        started_threads = []
        original_start = Thread.start

        def remember_thread(thread):
            started_threads.append(thread)
            original_start(thread)

        with (
            mock.patch.object(Thread, "start", remember_thread),
            mock.patch.object(threading, "excepthook") as mocked_excepthook,
        ):
            self.assertIs(service.process(), True)
            started_threads[0].join(timeout=5)

        mocked_excepthook.assert_called_once()
        self.assertIsInstance(mocked_excepthook.call_args.args[0].exc_value, SMTPServerDisconnected)

    def test_send_and_log_email_propagates_error(self):
        service = self._build_service(connection=mail.get_connection(backend=BROKEN_EMAIL_BACKEND))

        with self.assertRaisesMessage(SMTPServerDisconnected, "connection lost"):
            service._send_and_log_email(msg=service._build_mail_object())

    def test_send_and_log_email_stays_quiet_when_failing_silently(self):
        service = self._build_service(connection=mail.get_connection(backend=BROKEN_EMAIL_BACKEND, fail_silently=True))

        self.assertFalse(service._send_and_log_email(msg=service._build_mail_object()))

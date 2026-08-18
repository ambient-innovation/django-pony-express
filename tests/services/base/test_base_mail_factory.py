from smtplib import SMTPServerDisconnected
from threading import Thread
from unittest import mock

from django.core import mail
from django.test import TestCase

from django_pony_express.errors import EmailServiceConfigError
from django_pony_express.services.asynchronous.thread import ThreadEmailService
from django_pony_express.services.base import BaseEmailService, BaseEmailServiceFactory


class BaseEmailServiceFactoryTest(TestCase):
    class TestMailService(BaseEmailService):
        subject = "My subject"
        template_name = "testapp/test_email.html"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_init_recipient_list_is_set(self):
        email = "albertus.magnus@example.com"
        factory = BaseEmailServiceFactory([email])
        self.assertEqual(factory.recipient_email_list, [email])

    def test_is_valid_positive_case(self):
        email = "albertus.magnus@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email])
        factory.service_class = BaseEmailService
        self.assertTrue(factory.is_valid())

    def test_is_valid_no_recipients(self):
        factory = BaseEmailServiceFactory()
        factory.service_class = BaseEmailService
        with self.assertRaises(EmailServiceConfigError):
            factory.is_valid()

    def test_is_valid_no_service_class(self):
        email = "albertus.magnus@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email])
        with self.assertRaises(EmailServiceConfigError):
            factory.is_valid()

    def test_is_valid_no_exception_raised(self):
        factory = BaseEmailServiceFactory()
        factory.is_valid(raise_exception=False)
        self.assertEqual(len(factory.errors), 2)

    def test_has_errors_positive_case(self):
        factory = BaseEmailServiceFactory()
        factory.is_valid(raise_exception=False)
        self.assertTrue(factory.has_errors())

    def test_has_errors_negative_case(self):
        email = "albertus.magnus@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email])
        factory.service_class = BaseEmailService
        self.assertFalse(factory.has_errors())

    def test_get_recipient_list_regular(self):
        email_1 = "albertus.magnus@example.com"
        email_2 = "thomas.von.aquin@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email_1, email_2])
        self.assertEqual(factory.get_recipient_list(), [email_1, email_2])

    def test_get_email_from_recipient_regular(self):
        email_1 = "albertus.magnus@example.com"
        email_2 = "thomas.von.aquin@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email_1, email_2])
        self.assertEqual(factory.get_email_from_recipient(factory.get_recipient_list()[1]), email_2)

    def test_get_context_data_regular(self):
        factory = BaseEmailServiceFactory()
        self.assertEqual(factory.get_context_data(), {})

    def test_process_regular(self):
        email_1 = "albertus.magnus@example.com"
        email_2 = "thomas.von.aquin@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email_1, email_2])
        factory.service_class = self.TestMailService
        self.assertEqual(factory.process(), 2)

    @mock.patch.object(BaseEmailService, "process", return_value=False)
    def test_process_counts_sent_emails_only(self, *args):
        email_1 = "albertus.magnus@example.com"
        email_2 = "thomas.von.aquin@example.com"
        factory = BaseEmailServiceFactory(recipient_email_list=[email_1, email_2])
        factory.service_class = self.TestMailService
        self.assertEqual(factory.process(), 0)

    @mock.patch.object(Thread, "start")
    def test_process_counts_emails_handed_over_to_a_thread(self, mocked_start):
        class ThreadMailService(ThreadEmailService):
            subject = "My subject"
            template_name = "testapp/test_email.html"

        factory = BaseEmailServiceFactory(
            recipient_email_list=["albertus.magnus@example.com", "thomas.von.aquin@example.com"]
        )
        factory.service_class = ThreadMailService

        self.assertEqual(factory.process(), 2)
        self.assertEqual(mocked_start.call_count, 2)

    def test_process_uses_connection_of_service_class(self):
        class SilentMailService(self.TestMailService):
            connection = mail.get_connection(backend="testapp.mail_backends.BrokenEmailBackend", fail_silently=True)

        factory = BaseEmailServiceFactory(recipient_email_list=["albertus.magnus@example.com"])
        factory.service_class = SilentMailService

        self.assertEqual(factory.process(), 0)

    def test_process_propagates_send_errors(self):
        class BrokenMailService(self.TestMailService):
            def _send_and_log_email(self, msg):
                raise SMTPServerDisconnected("connection lost")

        factory = BaseEmailServiceFactory(recipient_email_list=["albertus.magnus@example.com"])
        factory.service_class = BrokenMailService

        with self.assertRaisesMessage(SMTPServerDisconnected, "connection lost"):
            factory.process()

    def test_process_with_exception(self):
        factory = BaseEmailServiceFactory()
        factory.service_class = self.TestMailService
        with self.assertRaises(EmailServiceConfigError):
            factory.process()

    @mock.patch.object(BaseEmailServiceFactory, "is_valid", return_value=False)
    def test_process_is_valid_invalid(self, *args):
        factory = BaseEmailServiceFactory()
        factory.service_class = self.TestMailService
        self.assertEqual(factory.process(), 0)

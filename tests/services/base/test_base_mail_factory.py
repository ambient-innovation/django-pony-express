from django.test import TestCase

from django_pony_express.errors import EmailServiceConfigError
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

    def test_process_with_exception(self):
        factory = BaseEmailServiceFactory()
        factory.service_class = self.TestMailService
        with self.assertRaises(EmailServiceConfigError):
            factory.process()

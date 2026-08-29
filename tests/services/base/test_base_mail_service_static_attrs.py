from django.core import mail
from django.test import TestCase

from django_pony_express.errors import EmailServiceConfigError
from django_pony_express.services.base import BaseEmailService


class BaseEmailServiceStaticClassAttributeTest(TestCase):
    """Regression tests for GH issue #48.

    BaseEmailService.__init__() used to assign the constructor arguments
    unconditionally (``self.recipient_email_list = recipient_email_list or
    []``), so a subclass which declares ``recipient_email_list`` or
    ``attachment_list`` as a class attribute got an empty list instead: the
    ``or []`` fallback shadowed the class attribute with a fresh empty
    instance attribute whenever the kwarg was omitted, even though the
    documented API says the constructor argument "might be none, because
    you could set the variable statically in the class definition".
    """

    def test_statically_declared_recipient_list_survives_instantiation(self):
        class MyEmailService(BaseEmailService):
            subject = "My subject"
            template_name = "testapp/test_email.html"
            recipient_email_list = ["albertus.magnus@example.com"]

        service = MyEmailService()

        self.assertEqual(service.recipient_email_list, ["albertus.magnus@example.com"])
        # is_valid() must not raise now that the static list is honoured.
        self.assertTrue(service.is_valid())

    def test_statically_declared_attachment_list_survives_instantiation(self):
        class MyEmailService(BaseEmailService):
            subject = "My subject"
            template_name = "testapp/test_email.html"
            recipient_email_list = ["albertus.magnus@example.com"]
            attachment_list = ["/tmp/some.pdf"]

        service = MyEmailService()

        self.assertEqual(service.attachment_list, ["/tmp/some.pdf"])

    def test_explicit_kwarg_still_takes_precedence_over_class_attribute(self):
        class MyEmailService(BaseEmailService):
            subject = "My subject"
            template_name = "testapp/test_email.html"
            recipient_email_list = ["static@example.com"]

        service = MyEmailService(recipient_email_list=["explicit@example.com"])

        self.assertEqual(service.recipient_email_list, ["explicit@example.com"])

    def test_omitted_recipient_list_without_class_attribute_stays_empty(self):
        # No regression for the vanilla case: no static declaration, no
        # kwarg -> still an empty list, matching prior behavior.
        service = BaseEmailService()
        self.assertEqual(service.recipient_email_list, [])
        self.assertEqual(service.attachment_list, [])

    def test_static_default_is_not_shared_mutable_state_across_instances(self):
        class MyEmailService(BaseEmailService):
            subject = "My subject"
            template_name = "testapp/test_email.html"

        first = MyEmailService()
        second = MyEmailService()

        first.recipient_email_list.append("mutated@example.com")

        self.assertEqual(second.recipient_email_list, [])
        self.assertNotIn("mutated@example.com", MyEmailService.recipient_email_list)

    def test_end_to_end_send_uses_static_recipient_list(self):
        class MyEmailService(BaseEmailService):
            subject = "My subject"
            template_name = "testapp/test_email.html"
            recipient_email_list = ["dummy@example.com"]

        service = MyEmailService()
        result = service.process()

        self.assertIs(result, True)
        self.assertEqual(mail.outbox[0].to, ["dummy@example.com"])

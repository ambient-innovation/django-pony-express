import datetime
import logging
from os.path import basename
from unittest import mock

import time_machine
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase, override_settings
from django.utils import translation

from django_pony_express.errors import EmailServiceAttachmentError, EmailServiceConfigError
from django_pony_express.services.base import BaseEmailService


class BaseEmailServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_init_recipient_as_str_is_wrapped_to_list(self):
        email = "albertus.magnus@example.com"
        service = BaseEmailService(email)
        self.assertEqual(service.recipient_email_list, [email])

    def test_init_recipient_and_context_are_initialised_empty(self):
        service = BaseEmailService()
        self.assertEqual(service.recipient_email_list, [])
        self.assertEqual(service.context_data, {})

    def test_init_connection_regular(self):
        connection = mail.get_connection()

        service = BaseEmailService(recipient_email_list=["dummy@example.com"], connection=connection)

        service.subject = "My subject"
        service.template_name = "testapp/test_email.html"

        result = service.process()
        self.assertIs(result, 1)

        # Assert email was "sent"
        self.assertGreater(len(mail.outbox), 0)
        self.assertEqual(mail.outbox[0].subject, "My subject")
        self.assertEqual(mail.outbox[0].to, ["dummy@example.com"])

    def test_get_logger_logger_not_set(self):
        service = BaseEmailService()
        email_logger = service._get_logger()
        self.assertEqual(service._logger, email_logger)

    def test_get_logger_logger_set(self):
        service = BaseEmailService()
        service._logger = logging.getLogger("my_logger")
        email_logger = service._get_logger()
        self.assertEqual(service._logger, email_logger)

    def test_get_context_data_regular(self):
        data = {"city": "Cologne"}
        service = BaseEmailService(context_data=data)
        self.assertEqual(service.get_context_data(), data)

    def test_get_subject_no_prefix(self):
        subject = "I am a subject!"
        service = BaseEmailService()
        service.subject = subject
        self.assertEqual(service.get_subject(), subject)

    def test_get_subject_with_prefix(self):
        prefix = "Pony Express"
        subject = "I am a subject!"
        service = BaseEmailService()
        service.SUBJECT_PREFIX = prefix
        service.subject = subject
        self.assertIn(prefix, service.get_subject())
        self.assertIn(service.SUBJECT_DELIMITER, service.get_subject())
        self.assertIn(subject, service.get_subject())

    def test_get_subject_with_prefix_and_custom_delimiter(self):
        prefix = "Pony Express"
        custom_delimiter = " | "
        subject = "I am a subject!"
        service = BaseEmailService()
        service.SUBJECT_PREFIX = prefix
        service.SUBJECT_DELIMITER = custom_delimiter
        service.subject = subject
        self.assertIn(prefix, service.get_subject())
        self.assertIn(custom_delimiter, service.get_subject())
        self.assertIn(subject, service.get_subject())

    @override_settings(DEFAULT_FROM_EMAIL="noreply@example.com")
    def test_get_from_email_from_settings(self):
        service = BaseEmailService()
        self.assertEqual(service.get_from_email(), "noreply@example.com")

    @override_settings(DEFAULT_FROM_EMAIL="noreply@example.com")
    def test_get_from_email_from_class(self):
        email = "albertus.magnus@example.com"
        service = BaseEmailService()
        service.FROM_EMAIL = email
        self.assertEqual(service.get_from_email(), email)

    def test_get_reply_to_email_not_set(self):
        service = BaseEmailService()
        self.assertEqual(service.get_reply_to_emails(), [])

    def test_get_reply_to_email_is_set(self):
        email = "albertus.magnus@example.com"
        service = BaseEmailService()
        service.REPLY_TO_ADDRESS = email
        self.assertEqual(service.get_reply_to_emails(), [email])

    def test_get_cc_email_not_set(self):
        service = BaseEmailService()
        self.assertEqual(service.get_cc_emails(), [])

    def test_get_cc_email_is_set(self):
        email = "albertus.magnus@example.com"
        service = BaseEmailService()
        service.cc_email_list = [email]
        self.assertEqual(service.get_cc_emails(), [email])

    def test_get_bcc_email_not_set(self):
        service = BaseEmailService()
        self.assertEqual(service.get_bcc_emails(), [])

    def test_get_bcc_email_is_set(self):
        email = "albertus.magnus@example.com"
        service = BaseEmailService()
        service.bcc_email_list = [email]
        self.assertEqual(service.get_bcc_emails(), [email])

    @override_settings(LANGUAGE_CODE="de-AT")
    def test_get_translation_regular_german(self):
        service = BaseEmailService()
        self.assertEqual(service.get_translation(), "de")

    @override_settings(LANGUAGE_CODE="en-GB")
    def test_get_translation_regular_english(self):
        service = BaseEmailService()
        self.assertEqual(service.get_translation(), "en")

    @override_settings(LANGUAGE_CODE="de")
    def test_get_translation_settings_short(self):
        service = BaseEmailService()
        self.assertEqual(service.get_translation(), "de")

    @override_settings(LANGUAGE_CODE=None)
    def test_get_translation_settings_not_set(self):
        service = BaseEmailService()
        self.assertEqual(service.get_translation(), None)

    @override_settings(LANGUAGE_CODE=1)
    def test_get_translation_settings_invalid_type(self):
        service = BaseEmailService()
        self.assertEqual(service.get_translation(), None)

    @override_settings(LANGUAGE_CODE="a")
    def test_get_translation_settings_invalid_value(self):
        service = BaseEmailService()
        self.assertEqual(service.get_translation(), None)

    def test_get_attachments_regular(self):
        file_path = "usr/albertus/myfile.csv"
        service = BaseEmailService(attachment_list=[file_path])
        self.assertEqual(service.get_attachments(), [file_path])

    def test_get_attachments_empty(self):
        service = BaseEmailService()
        self.assertEqual(service.get_attachments(), [])

    def test_add_attachments_path_as_str(self):
        # Setup
        service = BaseEmailService()
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        file_path = settings.BASE_PATH / "tests/files/testfile.txt"
        service.attachment_list = [file_path]
        msg_obj = service._add_attachments(msg_obj)

        self.assertEqual(len(msg_obj.attachments), 1)
        self.assertEqual(msg_obj.attachments[0][0], basename(file_path))

    def test_add_attachments_path_as_dict(self):
        # Setup
        service = BaseEmailService()
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        filename = "awesome_file.txt"
        file_path = settings.BASE_PATH / "tests/files/testfile.txt"
        service.attachment_list = [{"filename": filename, "file": file_path, "mimetype": "text/text"}]
        msg_obj = service._add_attachments(msg_obj)

        self.assertEqual(len(msg_obj.attachments), 1)
        self.assertEqual(msg_obj.attachments[0][0], filename)

    def test_add_attachments_path_wrong_dict_data(self):
        # Setup
        service = BaseEmailService()
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        filename = "awesome_file.txt"
        service.attachment_list = [{"filename": filename}]

        with self.assertRaises(EmailServiceAttachmentError):
            service._add_attachments(msg_obj)

    @time_machine.travel(datetime.date(2020, 6, 26))
    def test_build_mail_object_regular(self):
        from_email = "noreply@example.com"
        reply_to_email = "willreply@example.com"
        email = "albertus.magnus@example.com"
        subject = "Test email"
        my_var = "Lorem ipsum dolor!"
        service = BaseEmailService(recipient_email_list=[email], context_data={"my_var": my_var})
        service.FROM_EMAIL = from_email
        service.REPLY_TO_ADDRESS = reply_to_email
        service.subject = subject
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        # Assertions
        self.assertIsInstance(msg_obj, EmailMultiAlternatives)

        self.assertEqual(msg_obj.subject, subject)

        self.assertEqual(msg_obj.from_email, from_email)
        self.assertEqual(msg_obj.to, [email])
        self.assertEqual(msg_obj.reply_to, [reply_to_email])

        self.assertIn("Friday", msg_obj.body)
        self.assertIn(my_var, msg_obj.body)

        self.assertIn("Friday", msg_obj.alternatives[0][0])
        self.assertIn(my_var, msg_obj.alternatives[0][0])

    def test_build_mail_object_with_attachments(self):
        from_email = "noreply@example.com"
        reply_to_email = "willreply@example.com"
        email = "albertus.magnus@example.com"
        subject = "Test email"
        my_var = "Lorem ipsum dolor!"
        file_path = settings.BASE_PATH / "tests/files/testfile.txt"
        service = BaseEmailService(
            recipient_email_list=[email], context_data={"my_var": my_var}, attachment_list=[file_path]
        )
        service.FROM_EMAIL = from_email
        service.REPLY_TO_ADDRESS = reply_to_email
        service.subject = subject
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        # Assertions
        self.assertIsInstance(msg_obj, EmailMultiAlternatives)

        self.assertEqual(len(msg_obj.attachments), 1)
        self.assertEqual(msg_obj.attachments[0][0], basename(file_path))

    @mock.patch.object(BaseEmailService, "get_translation", return_value=None)
    def test_build_mail_object_missing_language(self, *args):
        email = "albertus.magnus@example.com"
        my_var = "Lorem ipsum dolor!"
        file_path = settings.BASE_PATH / "tests/files/testfile.txt"
        service = BaseEmailService(
            recipient_email_list=[email], context_data={"my_var": my_var}, attachment_list=[file_path]
        )

        service.template_name = "testapp/test_email.html"

        with mock.patch.object(translation, "activate") as mocked_activate:
            service._build_mail_object()
            mocked_activate.assert_not_called()

    def test_setting_txt_templates_works(self):
        my_var = "Lorem ipsum dolor!"
        service = BaseEmailService(
            recipient_email_list=["albertus.magnus@example.com"], context_data={"my_var": my_var}
        )
        service.FROM_EMAIL = "noreply@example.com"
        service.subject = "Test mail"
        service.template_name = "testapp/test_email.html"
        service.template_txt_name = "testapp/test_email.txt"
        msg_obj = service._build_mail_object()

        # Assertions
        self.assertIsInstance(msg_obj, EmailMultiAlternatives)

        self.assertIn("I am a different content", msg_obj.body)
        self.assertNotIn("I am a different content", msg_obj.alternatives[0][0])

        self.assertIn(my_var, msg_obj.body)

    @time_machine.travel(datetime.date(2020, 6, 26))
    @override_settings(LANGUAGE_CODE="nl-BE")
    def test_build_mail_object_translation_works(self):
        service = BaseEmailService(recipient_email_list="noreply@example.com")
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        # Assertions
        self.assertIsInstance(msg_obj, EmailMultiAlternatives)

        self.assertIn("vrijdag", msg_obj.body)
        self.assertIn("vrijdag", msg_obj.alternatives[0][0])

    def test_check_email_structure_validity_valid_email(self):
        service = BaseEmailService()
        self.assertIs(service._check_email_structure_validity(email="albertus.magnus@example.com"), True)

    def test_check_email_structure_validity_invalid_email(self):
        service = BaseEmailService()
        self.assertIs(service._check_email_structure_validity(email="no-at-example.com"), False)

    @time_machine.travel(datetime.date(2020, 6, 26))
    @override_settings(LANGUAGE_CODE="de")
    @mock.patch.object(BaseEmailService, "get_translation", return_value="nl-BE")
    def test_build_mail_object_deactivates_language_afterwards(self, *args):
        service = BaseEmailService(recipient_email_list="noreply@example.com")
        service.template_name = "testapp/test_email.html"
        msg_obj = service._build_mail_object()

        # Assertions
        # Assert, that email was rendered in nl-BE language
        self.assertIn("vrijdag", msg_obj.body)
        self.assertIn("vrijdag", msg_obj.alternatives[0][0])

        # Assert, system language is back to "de"
        self.assertEqual(settings.LANGUAGE_CODE, "de")

    def test_is_valid_positive_case(self):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = BaseEmailService(recipient_email_list=[email])
        service.subject = subject
        service.template_name = "testapp/test_email.html"
        self.assertTrue(service.is_valid())

    def test_is_valid_no_subject(self):
        email = "albertus.magnus@example.com"
        service = BaseEmailService(recipient_email_list=[email])
        service.template_name = "testapp/test_email.html"
        with self.assertRaises(EmailServiceConfigError):
            service.is_valid()

    def test_is_valid_no_template(self):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = BaseEmailService(recipient_email_list=[email])
        service.subject = subject
        with self.assertRaises(EmailServiceConfigError):
            service.is_valid()

    def test_is_valid_no_recipient(self):
        subject = "Test email"
        service = BaseEmailService()
        service.subject = subject
        with self.assertRaises(EmailServiceConfigError):
            service.is_valid()

    def test_is_valid_no_exception_raised(self):
        service = BaseEmailService()
        service.is_valid(raise_exception=False)
        self.assertEqual(len(service.errors), 3)

    def test_is_valid_invalid_email_address(self):
        service = BaseEmailService()
        service.subject = "My subject"
        service.template_name = "testapp/test_email.html"
        service.recipient_email_list = ["test user@example.com"]

        service.is_valid(raise_exception=False)

        self.assertEqual(len(service.errors), 1)
        self.assertIn('Email service received ill-formatted email address "test user@example.com"', service.errors)

    def test_has_errors_positive_case(self):
        service = BaseEmailService()
        service.is_valid(raise_exception=False)
        self.assertTrue(service.has_errors())

    def test_has_errors_negative_case(self):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = BaseEmailService(recipient_email_list=[email])
        service.subject = subject
        service.template_name = "testapp/test_email.html"
        self.assertFalse(service.has_errors())

    @mock.patch("django_pony_express.services.base.BaseEmailService._logger")
    def test_send_and_log_email_success_privacy_active(self, mock_logger):
        service = BaseEmailService(recipient_email_list=["thomas.aquin@example.com"])
        result = service._send_and_log_email(
            msg=EmailMultiAlternatives(subject="The Pony Express", to=["thomas.aquin@example.com"])
        )

        mock_logger.info.assert_called_with('Email "The Pony Express" successfully sent.')
        self.assertEqual(result, 1)

    @mock.patch("django_pony_express.services.base.BaseEmailService._logger")
    @mock.patch("django_pony_express.services.base.PONY_LOG_RECIPIENTS", True)
    def test_send_and_log_success_privacy_inactive(self, mock_logger):
        service = BaseEmailService(recipient_email_list=["thomas.aquin@example.com"])
        result = service._send_and_log_email(
            msg=EmailMultiAlternatives(subject="The Pony Express", to=["thomas.aquin@example.com"])
        )

        mock_logger.info.assert_called_with('Email "The Pony Express" successfully sent to thomas.aquin@example.com.')
        self.assertEqual(result, 1)

    @mock.patch.object(EmailMultiAlternatives, "send", side_effect=Exception("Broken pony"))
    @mock.patch("django_pony_express.services.base.BaseEmailService._logger")
    def test_send_and_log_email_failure_privacy_active(self, mock_logger, *args):
        service = BaseEmailService(recipient_email_list=["thomas.aquin@example.com"])
        result = service._send_and_log_email(
            msg=EmailMultiAlternatives(subject="The Pony Express", to=["thomas.aquin@example.com"])
        )

        mock_logger.error('An error occurred sending email "%s": %s', "The Pony Express", "Broken pony")
        self.assertFalse(result)

    @mock.patch.object(EmailMultiAlternatives, "send", side_effect=Exception("Broken pony"))
    @mock.patch("django_pony_express.services.base.BaseEmailService._logger")
    @mock.patch("django_pony_express.services.base.PONY_LOG_RECIPIENTS", True)
    def test_send_and_log_failure_privacy_inactive(self, mock_logger, *args):
        service = BaseEmailService(recipient_email_list=["thomas.aquin@example.com"])
        result = service._send_and_log_email(
            msg=EmailMultiAlternatives(subject="The Pony Express", to=["thomas.aquin@example.com"])
        )

        mock_logger.error(
            'An error occurred sending email "%s" to %s: %s',
            "The Pony Express",
            "thomas.aquin@example.com",
            "Broken pony",
        )
        self.assertFalse(result)

    def test_process_regular(self):
        email = "albertus.magnus@example.com"
        subject = "Test email"
        service = BaseEmailService(recipient_email_list=[email])
        service.subject = subject
        service.template_name = "testapp/test_email.html"
        self.assertTrue(service.process())

    def test_process_with_error(self):
        subject = "Test email"
        service = BaseEmailService()
        service.subject = subject
        service.template_name = "testapp/test_email.html"
        with self.assertRaises(EmailServiceConfigError):
            service.process()

    @mock.patch.object(BaseEmailService, "is_valid", return_value=False)
    def test_process_is_valid_invalid(self, *args):
        factory = BaseEmailService()
        self.assertEqual(factory.process(), 0)

    def test_html_templates_rendering(self):
        my_var = "Lorem ipsum dolor!"
        service = BaseEmailService()
        service.template_name = "testapp/test_email.html"
        msg_html = service._generate_html_content({"my_var": my_var})

        # Assertions
        self.assertIsInstance(msg_html, str)

        self.assertIn("Lorem ipsum dolor", msg_html)
        self.assertNotIn("I am a different content", msg_html)

    def test_text_templates_rendering(self):
        my_var = "Lorem ipsum dolor!"
        service = BaseEmailService()
        service.template_txt_name = "testapp/test_email.txt"
        msg_text = service._generate_text_content({"my_var": my_var}, "")

        # Assertions
        self.assertIsInstance(msg_text, str)

        self.assertIn("Lorem ipsum dolor", msg_text)
        self.assertIn("I am a different content", msg_text)
        self.assertNotIn("Current date test", msg_text)

    @time_machine.travel(datetime.date(2025, 6, 26))
    def test_generate_text_content_html_conversion(self):
        my_var = "Lorem ipsum dolor!"
        service = BaseEmailService()
        service.template_name = "testapp/test_email.html"

        msg_html = service._generate_html_content({"my_var": my_var, "link_url": "https//example.com?pony=horse"})
        msg_txt = service._generate_text_content(mail_attributes={}, html_content=msg_html)

        # Assertions
        self.assertIsInstance(msg_html, str)

        self.assertIn("Lorem ipsum dolor", msg_txt)
        # Check linebreaks are not removed
        self.assertIn("26. June 2025\n", msg_txt)

        # Check links are converted correctly
        self.assertIn("I am a link (https//example.com?pony=horse)", msg_txt)

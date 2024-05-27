import re

from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from django_pony_express.services.tests import EmailTestService, EmailTestServiceMail, EmailTestServiceQuerySet


class EmailTestServiceTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Mail data
        cls.subject = "Super great email (definitely not spam!)"
        cls.to = "spam@world.com"
        cls.cc = "spam-copy@world.com"
        cls.bcc = "spam-secret@world.com"
        cls.content_part = "body part"
        cls.text_content = "I'm the %s." % cls.content_part
        cls.html_content = "<html>I'm the %s.</html>" % cls.content_part

        cls.other_mail_subject = "Other mail subject"

        # Initialize django outbox
        mail.outbox = []

        # Instances
        cls.ets = EmailTestService()

    def setUp(self):
        super().setUp()

        # Create email per test case
        email = EmailMultiAlternatives(self.subject, self.text_content, to=[self.to], cc=[self.cc], bcc=[self.bcc])
        email.attach_alternative(self.html_content, "text/html")
        mail.outbox.append(email)

        # Create second email per test case
        email = EmailMultiAlternatives(
            self.other_mail_subject, self.text_content, to=["to@world.com"], cc=["cc@world.com"], bcc=["bcc@world.com"]
        )
        email.attach_alternative(self.html_content, "text/html")
        mail.outbox.append(email)

    def tearDown(self) -> None:
        super().tearDown()
        # Emtpy mailbox for next test
        mail.outbox = []

    def test_outbox_is_updated(self):
        self.assertEqual(self.ets.all().count(), 2)
        # Create third mail
        email = EmailMultiAlternatives(
            self.other_mail_subject, self.text_content, to=["to@world.com"], cc=["cc@world.com"], bcc=["bcc@world.com"]
        )
        email.attach_alternative(self.html_content, "text/html")
        mail.outbox.append(email)
        self.assertEqual(self.ets.all().count(), 3)

    def test_ensure_outbox_is_loaded(self):
        ets = EmailTestService()
        self.assertEqual(ets._outbox, None)
        ets._ensure_outbox_is_loaded()
        self.assertIsInstance(ets._outbox, list)

    def test_reload(self):
        ets = EmailTestService()
        self.assertEqual(ets._outbox, None)
        ets.reload()
        self.assertIsInstance(ets._outbox, list)

    def test_filter_no_params(self):
        self.assertRaises(ValueError, self.ets.filter)

    def test_filter_to_valid(self):
        qs = self.ets.filter(to=self.to)
        self.assertEqual(qs.count(), 1)

    def test_filter_cc_valid(self):
        qs = self.ets.filter(cc=self.cc)
        self.assertEqual(qs.count(), 1)

    def test_filter_bcc_valid(self):
        qs = self.ets.filter(bcc=self.bcc)
        self.assertEqual(qs.count(), 1)

    def test_filter_subject_valid(self):
        qs = self.ets.filter(subject=self.subject)
        self.assertEqual(qs.count(), 1)

    def test_filter_to_invalid(self):
        qs = self.ets.filter(to="not-my@mail.com")
        self.assertEqual(qs.count(), 0)

    def test_filter_cc_invalid(self):
        qs = self.ets.filter(cc="not-my@mail.com")
        self.assertEqual(qs.count(), 0)

    def test_filter_bcc_invalid(self):
        qs = self.ets.filter(bcc="not-my@mail.com")
        self.assertEqual(qs.count(), 0)

    def test_filter_subject_invalid(self):
        qs = self.ets.filter(subject="Not my subject")
        self.assertEqual(qs.count(), 0)

    def test_filter_to_cc_valid(self):
        qs = self.ets.filter(to=self.to, cc=self.cc)
        self.assertEqual(qs.count(), 1)

    def test_filter_to_cc_bcc_valid(self):
        qs = self.ets.filter(to=self.to, cc=self.cc, bcc=self.bcc)
        self.assertEqual(qs.count(), 1)

    def test_filter_to_cc_bcc_subject_valid(self):
        qs = self.ets.filter(to=self.to, cc=self.cc, bcc=self.bcc, subject=self.subject)
        self.assertEqual(qs.count(), 1)

    def test_filter_to_cc_bcc_subject_invalid(self):
        qs = self.ets.filter(to=self.to, cc=self.cc, bcc=self.bcc, subject="Not my subject")
        self.assertEqual(qs.count(), 0)

    def test_filter_subject_regular(self):
        qs = self.ets.filter(subject=self.subject)
        self.assertEqual(qs.count(), 1)

    def test_filter_subject_regex_invalid(self):
        qs = self.ets.filter(subject=re.compile("Not my subject"))
        self.assertEqual(qs.count(), 0)

    def test_filter_subject_translatable(self):
        qs = self.ets.filter(subject=_(self.subject))
        self.assertEqual(qs.count(), 1)

    def test_filter_subject_regex_valid_single(self):
        qs = self.ets.filter(subject=re.compile("definitely not"))
        self.assertEqual(qs.count(), 1)

    def test_filter_subject_regex_valid_multiple(self):
        qs = self.ets.filter(subject=re.compile("other|spam", flags=re.IGNORECASE))
        self.assertEqual(qs.count(), 2)

    def test_all(self):
        # Assertion
        self.assertEqual(self.ets.all().count(), 2)

    def test_validate_lookup_cache_contains_one_element_true(self):
        # Assertion (we have two mails so it's not equal to 1)
        self.assertEqual(self.ets.all().count(), 2)
        self.assertRaises(RuntimeError, self.ets.all()._validate_lookup_cache_contains_one_element)

    def test_validate_lookup_cache_contains_one_element_false(self):
        self.assertEqual(self.ets.filter(subject=self.subject).count(), 1)
        self.assertEqual(self.ets.filter(subject=self.subject)._validate_lookup_cache_contains_one_element(), None)

    def test_ensure_matching_list_was_populated_false(self):
        self.assertRaises(RuntimeError, EmailTestServiceQuerySet()._ensure_matching_list_was_populated)

    def test_ensure_matching_list_was_populated_true(self):
        self.assertEqual(self.ets.all()._ensure_matching_list_was_populated(), None)

    def test_get_html_content(self):
        self.assertEqual(self.ets.filter(subject=self.subject)._get_html_content(), self.html_content)

    def test_get_txt_content(self):
        self.assertEqual(self.ets.filter(subject=self.subject)._get_txt_content(), self.text_content)

    def test_one_true(self):
        self.assertEqual(self.ets.filter(subject=self.subject).one(), True)

    def test_one_false(self):
        self.assertEqual(self.ets.all().one(), False)

    def test_count(self):
        self.assertEqual(self.ets.all().count(), 2)
        self.assertEqual(self.ets.filter(subject=self.subject).count(), 1)
        self.assertEqual(self.ets.filter(subject="Not my subject").count(), 0)

    def test_first(self):
        self.assertEqual(self.ets.all().first().subject, self.subject)

    def test_last(self):
        self.assertEqual(self.ets.all().last().subject, self.other_mail_subject)

    def test_assert_one_true(self):
        self.ets.filter(subject=self.subject).assert_one()

    def test_assert_one_false(self):
        with self.assertRaises(AssertionError):
            self.ets.all().assert_one()

    def test_assert_quantity_true(self):
        self.ets.filter(subject=self.subject).assert_quantity(1)

    def test_assert_quantity_false(self):
        with self.assertRaises(AssertionError):
            self.ets.filter(subject=self.subject).assert_quantity(0)

    def test_assert_subject_true(self):
        self.ets.filter(subject=self.subject)[0].assert_subject(self.subject)

    def test_assert_subject_false(self):
        with self.assertRaises(AssertionError):
            self.ets.filter(subject=self.subject)[0].assert_subject(self.other_mail_subject)

    def test_assert_body_contains_true(self):
        self.ets.filter(subject=self.subject)[0].assert_body_contains(self.content_part)

    def test_assert_body_contains_false(self):
        with self.assertRaises(AssertionError):
            self.ets.filter(subject=self.subject)[0].assert_body_contains("Not in here!")

    def test_assert_body_contains_not_true(self):
        self.ets.filter(subject=self.subject)[0].assert_body_contains_not("Not in here!")

    def test_assert_body_contains_not_false(self):
        with self.assertRaises(AssertionError):
            self.ets.filter(subject=self.subject)[0].assert_body_contains_not(self.content_part)

    def test_assert_body_contains_no_html_part(self):
        subject = "No html email"
        email = EmailMultiAlternatives(subject, self.text_content, to=[self.to], cc=[self.cc], bcc=[self.bcc])
        mail.outbox.append(email)

        self.ets.filter(subject=subject)[0].assert_body_contains(self.content_part)

    def test_can_get_mail_via_item(self):
        mail_qs = self.ets.all()
        self.assertIsInstance(mail_qs[0], EmailTestServiceMail)

    def test_can_get_first_email_via_brackets_operator(self):
        mail_qs = self.ets.all()
        self.assertEqual(mail_qs[0], mail_qs.first())

    def test_can_get_last_email_via_brackets_operator(self):
        mail_qs = self.ets.all()
        self.assertEqual(mail_qs[-1], mail_qs.last())

    def test_can_use_len_operator(self):
        mail_qs = self.ets.all()
        self.assertEqual(len(mail_qs), 2)

    def test_assert_to_contains(self):
        email = self.ets.all()[0]
        email.assert_to_contains(self.to)

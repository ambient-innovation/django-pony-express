import re
import warnings
from typing import Optional, Union

from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase


class EmailTestService:
    _outbox = None

    def _ensure_outbox_is_loaded(self) -> None:
        """
        Ensures that the outbox attribute is set
        """
        if self._outbox is None:
            self.reload()

    def reload(self) -> None:
        """
        Loads the current _outbox inside an attribute of this class
        """
        self._outbox = mail.outbox

    def empty(self) -> None:
        """
        Empties the current outbox
        """
        mail.outbox = []
        self.reload()

    def filter(
        self,
        to: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        subject: Union[str, re.Pattern, None] = None,
    ) -> "EmailTestServiceQuerySet":
        """
        Searches in the _outbox for emails matching either to and/or subject.
        Returns a list of email objects
        """
        # Ensure that outbox is up to date
        self.reload()

        if not any([to, cc, bcc, subject]):
            raise ValueError("EmailTestService.filter called without parameters")

        if subject and not isinstance(subject, re.Pattern):
            # If the "subject" is a translatable, we have to cast it to string
            subject = re.compile(f"^{re.escape(str(subject))}$")

        match_list = []
        for email in self._outbox:
            # Check conditions
            match = True
            if to and to not in email.to:
                match = False
            if cc and cc not in email.cc:
                match = False
            if bcc and bcc not in email.bcc:
                match = False
            if subject and not re.search(subject, str(email.subject)):
                match = False

            # Add email if all set conditions are valid
            if match:
                match_list.append(email)

        return EmailTestServiceQuerySet(matching_list=match_list)

    def all(self) -> "EmailTestServiceQuerySet":
        """
        Loads all mails from the outbox inside the matching list
        """
        # Ensure that outbox is up to date
        self.reload()

        # Load data to matching list
        match_list = list(self._outbox)

        return EmailTestServiceQuerySet(matching_list=match_list)


class EmailTestServiceMail(mail.EmailMultiAlternatives):
    """
    Wrapper around a Django EmailMultiAlternatives object with some helper functions to write clean assertions.
    """

    _testcase = TestCase()  # Hacky way to get access to TestCase.assert* methods without deriving from TestCase

    def _get_html_content(self) -> Optional[str]:
        """
        Ensure we just have found one element and then return the HTML part of the email
        """
        # Search for string
        if len(self.alternatives) > 0:
            return self.alternatives[0][0]
        return None

    def _get_txt_content(self) -> str:
        """
        Ensure we just have found one element and then return the text part of the email
        """
        # Search for string
        return self.body

    def assert_subject(self, subject: str, msg: Optional[str] = None) -> None:
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        """

        # Assert the expected subject is equal to the generated one
        self._testcase.assertEqual(subject, self.subject, msg=msg)

    def assert_body_contains(self, search_str: str, msg: Optional[str] = None) -> None:
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        """

        # TODO: use Django 5.2 `body_contains()` once we drop older versions
        #  (https://docs.djangoproject.com/en/5.2/topics/email/#django.core.mail.EmailMultiAlternatives.body_contains)
        # Assert string is contained in TXT part
        self._testcase.assertIn(search_str, self._get_txt_content(), msg=msg)
        # Assert string is contained in HTML part (if HTML part is set)
        html_content = self._get_html_content()
        if html_content is not None:
            self._testcase.assertIn(search_str, html_content, msg=msg)

    def assert_body_contains_not(self, search_str: str, msg: Optional[str] = None) -> None:
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        """

        # Assert string is contained in the HTML part
        self._testcase.assertNotIn(search_str, self._get_html_content(), msg=msg)
        # Assert string is contained in the TXT part
        self._testcase.assertNotIn(search_str, self._get_txt_content(), msg=msg)

    def assert_to_contains(self, *emails: list[str]) -> None:
        """
        Searches in all given email for a specific email address in the "to"
        """
        for email in emails:
            self._testcase.assertIn(email, self.to)


class EmailTestServiceQuerySet(TestCase):
    _match_list = None

    def __init__(self, matching_list: Optional[list] = None) -> None:
        super().__init__()
        self._match_list = matching_list
        for email in self._match_list or []:
            # Change the class of every EmailMultiAlternative instance so that it points to
            # our subclass, which has some additional assertion-methods.
            if isinstance(email, EmailMultiAlternatives):
                email.__class__ = EmailTestServiceMail

    def _get_html_content(self) -> Optional[str]:
        """
        Ensure we just have found one element and then return the HTML part of the email
        """
        self._validate_lookup_cache_contains_one_element()
        # Search for string
        if len(self[0].alternatives) > 0:
            return self[0].alternatives[0][0]
        return None

    def _get_txt_content(self) -> str:
        """
        Ensure we just have found one element and then return the text part of the email
        """
        # Search for string
        self._validate_lookup_cache_contains_one_element()
        return self[0].body

    def _validate_lookup_cache_contains_one_element(self) -> None:
        """
        Ensures that in the cached lookup is exactly one element. Needed for full-text-search.
        """
        if self.count() > 1:
            raise RuntimeError("Current lookup has more than one email object and is thus ambiguous.")
        elif self.count() == 0:
            raise RuntimeError("Current lookup has zero matches so lookup does not make sense.")

    def _ensure_matching_list_was_populated(self) -> None:
        """
        Make sure that we queried at least once before working with the results
        """
        if self._match_list is None:
            raise RuntimeError(
                "Counting of matches called without previous query. Please call filter() or all() first."
            )

    def one(self) -> bool:
        """
        Checks if the previous query returned exactly one element
        """
        return self.count() == 1

    def count(self) -> int:
        """
        Returns the number of matches found by a previous call of `find()`
        """
        # Ensure list was queried before using results
        self._ensure_matching_list_was_populated()

        # Count matches
        return len(self)

    def first(self) -> EmailMultiAlternatives:
        """
        Returns the first found element
        """
        # Ensure list was queried before using results
        self._ensure_matching_list_was_populated()
        return self[0] if self.count() > 0 else False

    def last(self) -> EmailMultiAlternatives:
        """
        Returns the last found element
        """
        # Ensure list was queried before using results
        self._ensure_matching_list_was_populated()
        return self[-1] if self.count() > 0 else False

    def assert_one(self, msg: Optional[str] = None):
        """
        Makes an assertion to make sure the queried element exists exactly once
        """
        self.assertEqual(self.one(), True, msg=msg)

    def assert_quantity(self, target_quantity: str, msg: Optional[str] = None) -> None:
        """
        Makes an assertion to make sure that the number of queried mails is equal to `target_quantity`
        """
        self.assertEqual(self.count(), target_quantity, msg=msg)

    def assert_subject(self, subject: str, msg: Optional[str] = None) -> None:
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        """
        warnings.warn(
            "EmailTestServiceQuerySet.assert_subject is deprecated. Use queryset[0].assert_subject instead.",
            stacklevel=2,
        )
        # Ensure we just have found one element
        self._validate_lookup_cache_contains_one_element()
        self[0].assert_subject(subject, msg)

    def assert_body_contains(self, search_str: str, msg: Optional[str] = None) -> None:
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        """
        warnings.warn(
            "EmailTestServiceQuerySet.assert_body_contains is deprecated. "
            "Use queryset[0].assert_body_contains instead.",
            stacklevel=2,
        )
        # Ensure we just have found one element
        self._validate_lookup_cache_contains_one_element()
        self[0].assert_body_contains(search_str, msg)

    def assert_body_contains_not(self, search_str: str, msg: Optional[str] = None) -> None:
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        """
        warnings.warn(
            "EmailTestServiceQuerySet.assert_body_contains is deprecated. "
            "Use queryset[0].assert_body_contains_not instead.",
            stacklevel=2,
        )
        # Ensure we just have found one element
        self._validate_lookup_cache_contains_one_element()
        self[0].assert_body_contains_not(search_str, msg)

    def __getitem__(self, item) -> EmailTestServiceMail:
        return self._match_list.__getitem__(item)

    def __len__(self) -> int:
        return self._match_list.__len__()

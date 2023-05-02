from typing import Union

import html2text
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from ..errors import EmailServiceAttachmentError, EmailServiceConfigError


class BaseEmailServiceFactory:
    """
    Factory for creating emails of the same type but with recipient-dependent content.
    """

    _errors = []

    service_class = None
    recipient_email_list = []

    def __init__(self, recipient_email_list: Union[list, QuerySet] = None, **kwargs) -> None:
        """
        Initialisation takes optionally a list of recipients. Doesn't have to be a list of strings because
        fetching the actual email from a complex data structure can be done in the method `get_email_from_recipient()`
        """
        # Empty error list on initialisation
        self._errors = []

        super().__init__()
        if recipient_email_list:
            self.recipient_email_list = recipient_email_list

    def is_valid(self, raise_exception: bool = True) -> bool:
        """
        This function ensures that all required variables for the email object are set. Can be overridden and extended
        but again, make sure that super() is called
        """
        if not self.service_class:
            self._errors.append(_('Email factory requires a mail service class.'))
        if not len(self.get_recipient_list()):
            self._errors.append(_('Email factory requires a target mail address.'))

        if self._errors and raise_exception:
            raise EmailServiceConfigError(self._errors)

        return not bool(len(self._errors))

    def get_recipient_list(self) -> list:
        """
        Fetches the recipient list. Provided as a method to be able to customise it in the derived class.
        """
        return self.recipient_email_list

    def get_email_from_recipient(self, recipient) -> str:
        """
        Fetches the email from the recipient. Sometimes a list of mail addresses is passed, so we just have to
        return the current variable. But if we get a database object, we need to extract the email first.
        For example: `return user.email`
        """
        return recipient

    def get_context_data(self) -> dict:
        """
        Fetch context data required equally for every email created by the factory.
        """
        return {}

    def has_errors(self) -> bool:
        """
        Check if any errors are stored inside this class instance
        """
        return bool(len(self._errors))

    @property
    def errors(self) -> list:
        """
        Getter for fetching the stored error messages.
        Errors shall not be set manually, that's why we use a property here.
        """
        return self._errors

    def process(self, raise_exception: bool = True) -> int:
        """
        Create an email of `self.service_class` for every recipient. Per-email logic like setting the salutation
        is handled within each email class.
        Returns the number of sent emails.
        """
        counter = 0
        if self.is_valid(raise_exception=raise_exception):
            for recipient in self.get_recipient_list():
                email_object = self.service_class(
                    recipient_email_list=[self.get_email_from_recipient(recipient)],
                    context_data={'recipient': recipient, **self.get_context_data()},
                )
                email_object.process()
                counter += 1

        return counter


class BaseEmailService:
    """
    Class for wrapping all required things for email creation.
    """

    SUBJECT_PREFIX = None
    FROM_EMAIL = None
    REPLY_TO_ADDRESS = []

    _errors = []

    subject = None
    template_name = None
    template_txt_name = None
    recipient_email_list = []
    cc_email_list = []
    bcc_email_list = []
    attachment_list = []

    def __init__(
        self,
        recipient_email_list: Union[list, str] = None,
        context_data: dict = None,
        attachment_list: list = None,
        **kwargs,
    ) -> None:
        """
        Initialisation takes a single or list of email addresses and some context data. This context data
        might be provided from the factory to avoid querying data more than necessary.
        """
        # Empty error list on initialisation
        self._errors = []

        super().__init__()

        # Ensure that a single email address is wrapped in a list so we can use it in the `to` kwarg.
        if isinstance(recipient_email_list, str):
            recipient_email_list = [recipient_email_list]

        self.recipient_email_list = recipient_email_list if recipient_email_list else []
        self.context_data = context_data if context_data else {}
        self.attachment_list = attachment_list if attachment_list else []

    def get_context_data(self) -> dict:
        """
        This method provides the required variables for the base email template. If more variables are required,
        just override this method and make sure, super() is called
        """
        return self.context_data

    def get_subject(self) -> str:
        """
        This method provides the subject of the email. Prefixes every subject to create a similar look and feel across
        emails. Can be overridden if required.
        """
        if self.SUBJECT_PREFIX:
            return f'{self.SUBJECT_PREFIX} - {self.subject}'
        return self.subject

    def get_from_email(self) -> str:
        """
        Use set `FROM_EMAIL` or the django base `DEFAULT_FROM_EMAIL` if it is not set
        """
        return self.FROM_EMAIL if self.FROM_EMAIL else settings.DEFAULT_FROM_EMAIL

    def get_cc_emails(self) -> list:
        """
        Returns a list of emails as a string which will be used in the "CC" field of the generated email.
        """
        return self.cc_email_list

    def get_bcc_emails(self) -> list:
        """
        Returns a list of emails as a string which will be used in the "BCC" field of the generated email.
        """
        return self.bcc_email_list

    def get_reply_to_emails(self) -> list:
        """
        Ensure "reply to" is a list
        """
        return [self.REPLY_TO_ADDRESS] if isinstance(self.REPLY_TO_ADDRESS, str) else self.REPLY_TO_ADDRESS

    def get_translation(self) -> Union[str, None]:
        """
        Tries to fetch the current translation from the django settings.
        """
        try:
            return settings.LANGUAGE_CODE[:2] if settings.LANGUAGE_CODE and len(settings.LANGUAGE_CODE) >= 2 else None
        except TypeError:
            return None

    def get_attachments(self) -> list:
        """
        Method to be overwritten. Returns a list of file-paths which will be attached to the newly created email.
        """
        return self.attachment_list

    def _add_attachments(self, msg: EmailMultiAlternatives):
        """
        Method to encapsulate logic of adding attachments to an email object.
        """
        for attachment in self.get_attachments():
            if isinstance(attachment, dict):
                try:
                    msg.attach(attachment['filename'], attachment['file'], attachment.get('mimetype', None))
                except KeyError as e:
                    raise EmailServiceAttachmentError(
                        _('Missing or mislabeled data provided for email attachment.')
                    ) from e
            else:
                msg.attach_file(attachment)

        return msg

    def _build_mail_object(self) -> EmailMultiAlternatives:
        """
        This method creates a mail object. It collects the required variables, sets the subject and makes sure that
        a "reply_to" is set for maximum convenience during the runtime.
        The plaintext part of the email is generated from the html to avoid maintaining duplicate templates.
        """
        # Optionally set translation language for date formatting etc.
        language = self.get_translation()
        if language:
            translation.activate(language)

        # Gather variables
        mail_attributes = self.get_context_data()

        # Render HTML body content
        html_content = render_to_string(self.template_name, mail_attributes)

        # Render TXT body part if a template is explicitly set, otherwise convert HTML template to plain text
        if not self.template_txt_name:
            h = html2text.HTML2Text()
            # Set body width to infinite to avoid weird line breaks
            h.body_width = 0
            text_content = h.handle(html_content)
        else:
            text_content = render_to_string(self.template_txt_name, mail_attributes)

        # Build mail object
        msg = EmailMultiAlternatives(
            self.get_subject(),
            text_content,
            from_email=self.get_from_email(),
            cc=self.get_cc_emails(),
            bcc=self.get_bcc_emails(),
            reply_to=self.get_reply_to_emails(),
            to=self.recipient_email_list,
        )
        msg.attach_alternative(html_content, "text/html")

        # Add attachments (if available)
        msg = self._add_attachments(msg)

        # Return mail object
        return msg

    def is_valid(self, raise_exception: bool = True) -> bool:
        """
        This function ensures that all required variables for the email object are set. Can be overridden and extended
        but again, make sure that super() is called.
        """
        if not self.get_subject():
            self._errors.append(_('Email service requires a subject.'))
        if not self.template_name:
            self._errors.append(_('Email service requires a template.'))
        if not len(self.recipient_email_list):
            self._errors.append(_('Email service requires a target mail address.'))

        if self._errors and raise_exception:
            raise EmailServiceConfigError(self._errors)

        return not bool(len(self._errors))

    def has_errors(self) -> bool:
        """
        Check if any errors are stored inside this class instance
        """
        return bool(len(self._errors))

    @property
    def errors(self) -> list:
        """
        Getter for fetching the stored error messages.
        Errors shall not be set manually, that's why we use a property here.
        """
        return self._errors

    def process(self, raise_exception: bool = True) -> bool:
        """
        Public method which is called to actually send an email. Calls validation first and returns the result of
        "msg.send()"
        """
        result = False
        if self.is_valid(raise_exception=raise_exception):
            msg = self._build_mail_object()
            result = msg.send()

        return result

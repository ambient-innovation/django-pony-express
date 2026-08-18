from smtplib import SMTPServerDisconnected

from django.core.mail.backends.base import BaseEmailBackend


class BrokenEmailBackend(BaseEmailBackend):
    """
    Backend which always fails, no matter what "fail_silently" is set to. Used to assert that the mail service and
    not the backend decides whether an error is propagated to the caller.
    """

    def send_messages(self, email_messages):
        raise SMTPServerDisconnected("connection lost")

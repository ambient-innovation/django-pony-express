import threading

from django_pony_express.services.base import BaseEmailService


class ThreadEmailService(BaseEmailService):
    """
    Service to send emails using Python threads to avoid blocking the main thread while talking to an external API
    """

    def process(self, raise_exception: bool = True) -> bool:
        """
        Public method which is called to actually send an email.
        Calls validation first and returns whether the email was handed over to a thread. Since the mail is sent
        asynchronously, we can't tell if it was delivered.
        For the same reason, errors can't be propagated to the caller. Instead, they surface via
        "threading.excepthook" (which error monitoring like Sentry picks up) after having been logged. Use a
        connection created with "fail_silently=True" if you want the thread to stay quiet.
        """
        if not self.is_valid(raise_exception=raise_exception):
            return False

        msg = self._build_mail_object()
        email_thread = threading.Thread(target=self._send_and_log_email, args=(msg,))
        email_thread.start()

        return True

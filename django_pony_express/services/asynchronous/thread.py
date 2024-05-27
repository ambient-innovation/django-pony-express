import threading

from django_pony_express.services.base import BaseEmailService


class ThreadEmailService(BaseEmailService):
    """
    Service to send emails using Python threads to avoid blocking the main thread while talking to an external API
    """

    def process(self, raise_exception: bool = True) -> None:
        """
        Public method which is called to actually send an email.
        Calls validation first and returns the result of "msg.send()"
        """
        if self.is_valid(raise_exception=raise_exception):
            msg = self._build_mail_object()
            email_thread = threading.Thread(target=self._send_and_log_email, args=(msg,))
            email_thread.start()

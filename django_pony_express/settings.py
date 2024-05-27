from django.conf import settings

PONY_LOGGER_NAME: str = getattr(settings, "DJANGO_PONY_EXPRESS_LOGGER_NAME", "django_pony_express")
PONY_LOG_RECIPIENTS: bool = getattr(settings, "DJANGO_PONY_EXPRESS_LOG_RECIPIENTS", False)

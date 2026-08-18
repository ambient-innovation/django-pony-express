# Configuration

## Default "FROM"

You can set a subject prefix, so that all your emails look more similar when setting the constant ``SUBJECT_PREFIX``.\
Additionally, you can define a custom `SUBJECT_DELIMITER`, which will be added between your custom `SUBJECT_PREFIX` and your `subject`.

If you wish to define a custom "from" email, you can do so via the ``FROM_EMAIL`` constant. Take care:
If you do not set it, the ``DEFAULT_FROM_EMAIL`` variable from the django settings is used.

## Error handling

Pony express follows django's `fail_silently` contract: an error occurring while sending is always logged, and it is
additionally propagated to the caller unless the connection used for sending was created with `fail_silently=True`.

Note that django creates connections with `fail_silently=False` by default. Therefore, not passing a connection at all
means that errors reach your code (and your error monitoring).

```python
from django.core.mail import get_connection

# Errors are raised (default)
MyMailService(recipient_email_list=["albertus.magnus@example.com"]).process()

# Errors are not raised, `process()` returns False
MyMailService(
    recipient_email_list=["albertus.magnus@example.com"],
    connection=get_connection(fail_silently=True),
).process()
```

Note that django's own backends already swallow errors internally when they were created with `fail_silently=True`. In
that case, they simply report that nothing was delivered, and you get a warning without a traceback. Pony express only
gets to decide for backends which raise regardless of the flag.

If you need to decide this differently, override `_should_fail_silently()` in your mail service.

```python
class MyMailService(BaseEmailService):
    def _should_fail_silently(self, msg) -> bool:
        return True
```

Take care not to confuse this with the `raise_exception` keyword argument of `process()` and `is_valid()`. That one only
governs *configuration* errors (`EmailServiceConfigError`), which happen before anything is sent.

Two things are worth knowing:

* `BaseEmailServiceFactory.process()` aborts the whole batch on the first failing recipient. A factory doesn't pass a
  connection to the services it creates, so if you want the batch to continue, override `get_connection()` in your
  service class.

  ```python
  class MyMailService(BaseEmailService):
      def get_connection(self):
          return get_connection(fail_silently=True)
  ```

  Create the connection inside the method rather than storing it in a class attribute. A connection kept at class
  level is shared by every instance in the process, and django's backends serialise every send through a per-instance
  lock, which would turn a threaded batch back into a sequential one.

* `ThreadEmailService` sends in a thread, so errors can't reach the caller. They surface via `threading.excepthook`
  after having been logged, which error monitoring tools like Sentry pick up. Its `process()` returns whether the email
  was handed over to a thread, not whether it was delivered.

## Logging

To enable basic logging, add the following block to your Django settings.

Note that in this example, we are only logging to the console.

```python
LOGGING = {
    "loggers": {
        "django_pony_express": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
```

If you want to customise the logger name, you can do so with this variable in your global Django settings file.

```python
DJANGO_PONY_EXPRESS_LOGGER_NAME = "my_email_logger"
```

## Privacy configuration

When debugging email problem, it's incredibly helpful to know the recipient. But logging sensitive personal data - often
unknowingly - is at least a bad practice and contradicts the "privacy by design" pattern.

Since it's very helpful and might be required to find bugs, it's possible to activate logging the recipient email
addresses.

The authors feel that if you consciously activate this flag, you know what you are doing and think about the
consequences.

```python
DJANGO_PONY_EXPRESS_LOG_RECIPIENTS = True
```

# Configuration

## Default "FROM"

You can set a subject prefix, so that all your emails look more similar when setting the constant ``SUBJECT_PREFIX``.

If you wish to define a custom "from" email, you can do so via the ``FROM_EMAIL`` constant. Take care:
If you do not set it, the ``DEFAULT_FROM_EMAIL`` variable from the django settings is used.

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

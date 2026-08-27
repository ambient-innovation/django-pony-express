# Changelog

**3.1.1** (2026-08-27)
  * Maintenance updates via ambient-package-update

**3.1.0** (2026-08-24)
  * Added the accessor `BaseEmailService.get_recipient_emails()`, which follows the `get_*()` convention of the
    other configurable attributes and is the override point for resolving the recipients dynamically

**3.0.0** (2026-08-18)
  * **Breaking change:** `BaseEmailService._send_and_log_email()` no longer swallows every error occurring while
    sending. Errors are still logged, but they are now propagated to the caller unless the used connection was created
    with `fail_silently=True`. Since django creates connections with `fail_silently=False` by default, this affects
    every service which doesn't explicitly pass a connection (#44)
  * **Breaking change:** `BaseEmailServiceFactory.process()` now only counts emails the service class reported as
    processed, instead of counting every attempt. Note that `ThreadEmailService` reports an email as processed once it
    was handed over to a thread, since it can't know whether it was delivered
  * Fixed a bug where `BaseEmailServiceFactory.process()` didn't pass `raise_exception` on to the emails it creates,
    so an invalid email aborted the batch even when the caller asked for `raise_exception=False`
  * **Breaking change:** `ThreadEmailService.process()` returns a boolean stating whether the email was handed over to
    a thread, instead of returning `None`
  * Added the accessor `BaseEmailService.get_connection()`, which follows the `get_*()` convention of the other
    configurable attributes and is the override point for providing a connection to services created by a factory
  * Fixed a bug where a mail which wasn't delivered (`msg.send()` returning `0`) was logged as "successfully sent".
    This case is logged as a warning now
  * Added the overridable hook `BaseEmailService._should_fail_silently()` to customise the new error handling
  * Added missing and updated outdated German translations

  *Migration notes:*
  * To keep the previous behaviour, pass a connection which fails silently:
    `MyEmailService(..., connection=get_connection(fail_silently=True))`
  * Batch sends via `BaseEmailServiceFactory` now abort on the first failing recipient. A factory doesn't pass a
    connection to the services it creates, so if you want the batch to continue, override `get_connection()` in your
    service class and return a connection created with `fail_silently=True`
  * `ThreadEmailService` can't propagate errors to the caller. They now surface via `threading.excepthook` (and
    therefore in your error monitoring) instead of being silently logged away

**2.8.1** (2026-07-03)
  * Updated company and maintainer information to "Beyonder Deutschland"

**2.8.0** (2026-07-03)
  * **Breaking change:** Dropped support for Python 3.10 (nearing end-of-life in October 2026)
  * Added support for Python 3.14
  * Added native uv support to the rendered Read the Docs configuration
  * Replaced the unmaintained "m2r2" documentation dependency with "sphinx-mdinclude"
  * Added a Code of Conduct, issue templates and a pull request template to rendered packages
  * Made the single-version CI and Read the Docs jobs track the newest supported Python version
  * Bumped rendered single-version jobs to Python 3.14
  * Added a cache suffix to the uv setup step to avoid CI cache namespace conflicts
  * Excluded unsupported Python/Django combinations (Python 3.14 with Django 4.2 and 5.2) from the rendered CI matrix
  * Fixed the rendered ruff target-version to track the minimum supported Python (matching requires-python) instead of the newest
  * Removed the stale .md source suffix from the rendered Sphinx config, since sphinx-mdinclude provides only the mdinclude directive (not a Markdown source parser)

**2.7.8** (2026-03-30)
  * Maintenance updates via ambient-package-update

**2.7.7** (2026-03-30)
  * Maintenance updates via ambient-package-update

**2.7.6** (2025-12-11)
  * Maintenance updates via ambient-package-update

**2.7.5** (2025-10-15)
  * Maintenance updates via ambient-package-update

**2.7.4** (2025-10-09)
  * Maintenance updates via ambient-package-update

**2.7.3** (2025-06-24)
  * Convert `msg.send()` result to boolean in `._send_and_log_email()`

**2.7.2** (2025-05-30)
  * Replaced freezegun with time_machine for tests
  * Maintenance updates via ambient-package-update

**2.7.1** (2025-05-29)
  * Fixed a bug where html-converted plain text would miss links

**2.7.0** (2025-05-21)
  * Replaced `html2text` with `beautifulsoup4` to make package available under MIT license
  * Switched back to MIT license
  * Added `CONTRIBUTING.md` file and removed contributing guidelines from readme
  * Maintenance updates via ambient-package-update

**2.6.3** (2025-05-09)
  * Replaced docstring type hints with proper Pythonic ones in test suit

**2.6.2** (2025-04-03)
  * Maintenance updates via ambient-package-update

**2.6.1** (2025-03-18)
  * Fixed a bug where translations were not deactivated after sending an email

**2.6.0** (2025-03-17)
  * Added check for email structure validity

**2.5.1** (2025-02-15)
  * Maintenance updates via ambient-package-update

**2.5.0** (2024-12-03)
  * Added connection param to `BaseEmailService` (Thx to @sk-rama)

**2.4.3** (2024-11-15)
  * Move logic to render HTML and text content to dedicated methods

**2.4.2** (2024-11-15)
  * Internal updates via `ambient-package-update`

**2.4.1** (2024-10-14)
  * Added Python 3.13 support
  * Added Djade linter to pre-commit
  * Improved GitHub action triggers
  * Updated dev dependencies and linters

**2.4.0** (2024-09-11)
  * Allow custom subject delimiter

**2.3.3** (2024-09-11)
  * Fixed coverage setup due to GitHub changes

**2.3.2** (2024-09-11)
  * Fixed package name

**2.3.1** (2024-08-12)
  * Fixed test matrix

**2.3.0** (2024-08-12)
  * Added Django 5.1 support

**2.2.2** (2024-07-18)
  * Added SECURITY.md
  * Updated linters
  * Internal updates via `ambient-package-update`

**2.2.1** (2024-07-16)
  * Updated GitHub actions

**2.2.0** (2024-07-15)
  * Dropped Python 3.8 support
  * Added multiple ruff linters

**2.1.3** (2024-06-21)
  * Linted docs with `blacken-docs` via `ambient-package-update`

**2.1.2** (2024-06-14)
  * Internal updates via `ambient-package-update`

**2.1.1** (2024-05-31)
  * Changed log-level to "info" for successful dispatching
  * Improved configuration docs

**2.1.0** (2024-05-27)
  * Added `ThreadEmailService` for simple async sending of emails
  * Added basic logging with privacy configuration to mail class
  * Restructured documentation
  * Restructured unit-tests
  * Minor test improvements

**2.0.0** (2024-04-11)
  * Dropped Django 3.2 & 4.1 support (via `ambient-package-update`)
  * Internal updates via `ambient-package-update`

**1.3.0** (2023-12-04)
  * Added Django 5.0 support

**1.2.5** (2023-11-13)
  * Fixed wrong import path in docs

**1.2.4** (2023-11-03)
  * Switched formatter from `black` to `ruff`

**1.2.3** (2023-10-20)
  * Linter updaters including code adjustments
  * Updates from ambient updater

**1.2.2** (2023-10-04)
  * Dependency to ambient updater updated

**1.2.1** (2023-10-04)
  * Downgraded Python to 3.11 for readthedocs.org

**1.2.0** (2023-10-04)
  * Added Python 3.12 support
  * Updated internal linter packages

**1.1.6** (2023-09-08)
  * Metadata update via ambient package updater

**1.1.5** (2023-09-08)
  * Metadata update via ambient package updater
  * Cleaned up test matrix

**1.1.4** (2023-08-31)
  * Fixed downloads badge

**1.1.3** (2023-08-31)
  * Improved type-hinting for constructor of `BaseEmailServiceFactory` and `BaseEmailService`

**1.1.2** (2023-08-14)
  * Updated linters and add more strict linting rules

**1.1.1** (2023-05-10)
  * Updated readme "maintenance" section
  * Updated package linters
  * Added release scripts for windows and UNIX

**1.1.0** (2023-05-04)
  * Support for Django 4.2 added

**1.0.2** (2023-05-04)
  * Updated documentation

**1.0.1** (2023-05-03)
  * Added missing translations
  * Updated documentation

**1.0.0** (2023-05-01)
  * Release as a separate package at PyPI (was before a part of [ai-django-core](https://pypi.org/project/ai-django-core/))

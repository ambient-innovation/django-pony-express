# Changelog

**2.7.2** (2025-05-29)
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

* *2.6.1* (2025-03-18)
  * Fixed a bug where translations were not deactivated after sending an email

* *2.6.0* (2025-03-17)
  * Added check for email structure validity

* *2.5.1* (2025-02-15)
  * Maintenance updates via ambient-package-update

* *2.5.0* (2024-12-03)
  * Added connection param to `BaseEmailService` (Thx to @sk-rama)

* *2.4.3* (2024-11-15)
  * Move logic to render HTML and text content to dedicated methods

* *2.4.2* (2024-11-15)
  * Internal updates via `ambient-package-update`

* *2.4.1* (2024-10-14)
  * Added Python 3.13 support
  * Added Djade linter to pre-commit
  * Improved GitHub action triggers
  * Updated dev dependencies and linters

* *2.4.0* (2024-09-11)
  * Allow custom subject delimiter

* *2.3.3* (2024-09-11)
  * Fixed coverage setup due to GitHub changes

* *2.3.2* (2024-09-11)
  * Fixed package name

* *2.3.1* (2024-08-12)
  * Fixed test matrix

* *2.3.0* (2024-08-12)
  * Added Django 5.1 support

* *2.2.2* (2024-07-18)
  * Added SECURITY.md
  * Updated linters
  * Internal updates via `ambient-package-update`

* *2.2.1* (2024-07-16)
  * Updated GitHub actions

* *2.2.0* (2024-07-15)
  * Dropped Python 3.8 support
  * Added multiple ruff linters

* *2.1.3* (2024-06-21)
  * Linted docs with `blacken-docs` via `ambient-package-update`

* *2.1.2* (2024-06-14)
  * Internal updates via `ambient-package-update`

* *2.1.1* (2024-05-31)
  * Changed log-level to "info" for successful dispatching
  * Improved configuration docs

* *2.1.0* (2024-05-27)
  * Added `ThreadEmailService` for simple async sending of emails
  * Added basic logging with privacy configuration to mail class
  * Restructured documentation
  * Restructured unit-tests
  * Minor test improvements

* *2.0.0* (2024-04-11)
  * Dropped Django 3.2 & 4.1 support (via `ambient-package-update`)
  * Internal updates via `ambient-package-update`

* *1.3.0** (2023-12-04)
  * Added Django 5.0 support

* *1.2.5** (2023-11-13)
  * Fixed wrong import path in docs

* *1.2.4** (2023-11-03)
  * Switched formatter from `black` to `ruff`

* *1.2.3** (2023-10-20)
  * Linter updaters including code adjustments
  * Updates from ambient updater

* *1.2.2** (2023-10-04)
  * Dependency to ambient updater updated

* *1.2.1** (2023-10-04)
  * Downgraded Python to 3.11 for readthedocs.org

* *1.2.0** (2023-10-04)
  * Added Python 3.12 support
  * Updated internal linter packages

* *1.1.6** (2023-09-08)
  * Metadata update via ambient package updater

* *1.1.5** (2023-09-08)
  * Metadata update via ambient package updater
  * Cleaned up test matrix

* **1.1.4** (2023-08-31)
  * Fixed downloads badge

* **1.1.3** (2023-08-31)
  * Improved type-hinting for constructor of `BaseEmailServiceFactory` and `BaseEmailService`

* **1.1.2** (2023-08-14)
  * Updated linters and add more strict linting rules

* **1.1.1** (2023-05-10)
  * Updated readme "maintenance" section
  * Updated package linters
  * Added release scripts for windows and UNIX

* **1.1.0** (2023-05-04)
  * Support for Django 4.2 added

* **1.0.2** (2023-05-04)
  * Updated documentation

* **1.0.1** (2023-05-03)
  * Added missing translations
  * Updated documentation

* **1.0.0** (2023-05-01)
  * Release as a separate package at PyPI (was before a part of [ai-django-core](https://pypi.org/project/ai-django-core/))

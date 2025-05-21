[![PyPI release](https://img.shields.io/pypi/v/django-pony-express.svg)](https://pypi.org/project/django-pony-express/)
[![Downloads](https://static.pepy.tech/badge/django-pony-express)](https://pepy.tech/project/django-pony-express)
[![Coverage](https://img.shields.io/badge/Coverage-100.0%25-success)](https://github.com/ambient-innovation/django-pony-express/actions?workflow=CI)
[![Linting](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coding Style](https://img.shields.io/badge/code%20style-Ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Documentation Status](https://readthedocs.org/projects/django-pony-express/badge/?version=latest)](https://django-pony-express.readthedocs.io/en/latest/?badge=latest)

Welcome to the **django-pony-express** - class-based emails for Django shipping with a full test
suite.

Similar to class-based view in Django core, this package provides a neat, DRY and testable (!) way to handle your
emails in Django.

* [PyPI](https://pypi.org/project/django-pony-express/)
* [GitHub](https://github.com/ambient-innovation/django-pony-express)
* [Full documentation](https://django-pony-express.readthedocs.io/en/latest/index.html)
* Creator & Maintainer: [Ambient Digital](https://ambient.digital/)


## Features

* Class-based structure for emails
   * Avoid duplicate low-level setup
   * Utilise inheritance and OOP benefits
   * No duplicated templates for HTML and plain-text
* Test suite to write proper unit-tests for your emails
   * Access your test outbox like a Django queryset

## Etymology

> The Pony Express was an American express mail service that used relays of horse-mounted riders. [...] During its
> 18 months of operation, the Pony Express reduced the time for messages to travel between the east and west US
> coast to about 10 days.
>
> https://en.wikipedia.org/wiki/Pony_Express

The name of this package combines the Django mascot (a pony) with a once quite successful mail service in the US.
Ingenious, right?

## Installation

- Install the package via pip:

  `pip install django-pony-express`

  or via pipenv:

  `pipenv install django-pony-express`

- Add module to `INSTALLED_APPS` within the main django `settings.py`:

    ```python
    INSTALLED_APPS = (
        # ...
        "django_pony_express",
    )
    ```



### Publish to ReadTheDocs.io

- Fetch the latest changes in GitHub mirror and push them
- Trigger new build at ReadTheDocs.io (follow instructions in admin panel at RTD) if the GitHub webhook is not yet set
  up.

### Publish to PyPi

- Update documentation about new/changed functionality

- Update the `Changelog`

- Increment version in main `__init__.py`

- Create pull request / merge to master

- This project uses the flit package to publish to PyPI. Thus, publishing should be as easy as running:
  ```
  flit publish
  ```

  To publish to TestPyPI use the following to ensure that you have set up your .pypirc as
  shown [here](https://flit.readthedocs.io/en/latest/upload.html#using-pypirc) and use the following command:

  ```
  flit publish --repository testpypi
  ```

### Maintenance

Please note that this package supports the [ambient-package-update](https://pypi.org/project/ambient-package-update/).
So you don't have to worry about the maintenance of this package. This updater is rendering all important
configuration and setup files. It works similar to well-known updaters like `pyupgrade` or `django-upgrade`.

To run an update, refer to the [documentation page](https://pypi.org/project/ambient-package-update/)
of the "ambient-package-update".


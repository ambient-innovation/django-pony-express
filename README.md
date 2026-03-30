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

[PyPI](https://pypi.org/project/django-pony-express/) • [GitHub](https://github.com/ambient-innovation/django-pony-express) • [Full documentation](https://django-pony-express.readthedocs.io/en/latest/index.html)

Creator & Maintainer: [Ambient Digital](https://ambient.digital/)

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

  or via uv:

  `uv add django-pony-express`

- Add module to `INSTALLED_APPS` within the main django `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "django_pony_express",
)
```

## Releasing a new version

Releases are fully automated. Push a version tag and the pipeline will build, sign with
[Sigstore](https://www.sigstore.dev/), publish to PyPI via
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/), and create a GitHub Release —
no API tokens needed.

```bash
git tag v<version>          # e.g. git tag v1.2.3
git push origin v<version>
```

Tags **must** start with `v`. Tags without the prefix won't trigger the pipeline.

### First-time setup

Before the pipeline can run for the first time, an admin must:

1. **Create GitHub Environment `pypi`**
   - Go to *Settings → Environments → New environment*, name it exactly `pypi`
   - Under *Deployment branches and tags*, add a tag rule with pattern `v*`
   - Optionally add required reviewers for a manual approval gate

2. **Configure PyPI Trusted Publisher**
   - Go to *PyPI → Project settings → Publishing → Add a new publisher*
   - Fill in: Owner `ambient-innovation`, Repository `django-pony-express`,
     Workflow `release.yml`, Environment `pypi`

### Publish to ReadTheDocs.io

- Fetch the latest changes in GitHub mirror and push them
- Trigger new build at ReadTheDocs.io (follow instructions in admin panel at RTD) if the GitHub webhook is not yet set
  up.

### Maintenance

Please note that this package supports the [ambient-package-update](https://pypi.org/project/ambient-package-update/).
So you don't have to worry about the maintenance of this package. This updater is rendering all important
configuration and setup files. It works similar to well-known updaters like `pyupgrade` or `django-upgrade`.

To run an update, refer to the [documentation page](https://pypi.org/project/ambient-package-update/)
of the "ambient-package-update".

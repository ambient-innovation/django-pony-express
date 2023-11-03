from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import (
    DEV_DEPENDENCIES,
    LICENSE_GPL,
    SUPPORTED_DJANGO_VERSIONS,
    SUPPORTED_PYTHON_VERSIONS,
)
from ambient_package_update.metadata.package import PackageMetadata
from ambient_package_update.metadata.readme import ReadmeContent
from ambient_package_update.metadata.ruff_ignored_inspection import RuffIgnoredInspection

METADATA = PackageMetadata(
    package_name="django_pony_express",
    authors=[
        PackageAuthor(
            name="Ambient Digital",
            email="hello@ambient.digital",
        ),
    ],
    company="Ambient Innovation: GmbH",
    license=LICENSE_GPL,
    license_year=2023,
    development_status="5 - Production/Stable",
    has_migrations=False,
    readme_content=ReadmeContent(
        tagline="""Welcome to the **django-pony-express** - class-based emails for Django shipping with a full test
suite.

Similar to class-based view in Django core, this package provides a neat, DRY and testable (!) way to handle your
emails in Django.""",
        content="""## Features

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
Ingenious, right?""",
    ),
    dependencies=[
        "Django>=3.2",
        "html2text>=2020.1.16",
    ],
    supported_django_versions=SUPPORTED_DJANGO_VERSIONS,
    supported_python_versions=SUPPORTED_PYTHON_VERSIONS,
    optional_dependencies={
        "dev": [
            *DEV_DEPENDENCIES,
        ],
    },
    ruff_ignore_list=[
        RuffIgnoredInspection(key="N999", comment="Project name contains underscore, not fixable"),
        RuffIgnoredInspection(key="A003", comment="Django attributes shadow python builtins"),
        RuffIgnoredInspection(key="DJ001", comment="Django model text-based fields shouldn't be nullable"),
        RuffIgnoredInspection(key="B905", comment="Can be enabled when Python <=3.9 support is dropped"),
    ],
)

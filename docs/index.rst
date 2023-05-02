django-pony-express
===================

Welcome to the **django-pony-express** - class-based emails for Django shipping with a full test suite.

Similar to class-based view in Django core, this package provides a neat, DRY and testable (!) way to handle your
emails in Django.

The package is published at pypi under the following link: `https://pypi.org/project/django-pony-express/ <https://pypi.org/project/django-pony-express/>`_

The package was created and is being maintained `Ambient Digital <https://ambient.digital>`_.

========
Features
========

* Class-based structure for emails
   * Avoid duplicate low-level setup
   * Utilise inheritance and OOP benefits
   * No duplicated templates for HTML and plain-text
* Test suite to write proper unit-tests for your emails
   * Access your test outbox like a Django queryset

============
Installation
============

To install django-pony-express:

* Install with pip: :code:`pip install django-pony-express`.
* Add :code:`django-pony-express` to INSTALLED_APPS.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   features/mail.md
   features/tests.md
   features/changelog.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

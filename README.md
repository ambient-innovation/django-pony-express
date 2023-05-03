[![pypi](https://img.shields.io/pypi/v/django-pony-express.svg)](https://pypi.python.org/pypi/django-pony-express/)
[![Downloads](https://pepy.tech/badge/django-pony-express)](https://pepy.tech/project/django-pony-express)
[![Documentation Status](https://readthedocs.org/projects/django-pony-express/badge/?version=latest)](https://django-pony-express.readthedocs.io/en/latest/?badge=latest)

**Class-based emails including a test suite for Django**

Full documentation for the project is available at [readthedocs.io](https://django-pony-express.readthedocs.io/en/latest/index.html).

Created and maintained by [Ambient Digital](https://ambient.digital).

---

# Etymology

> The Pony Express was an American express mail service that used relays of horse-mounted riders. [...] During its 18
> months of operation, the Pony Express reduced the time for messages to travel between the east and west US coast to
> about 10 days.
>
> https://en.wikipedia.org/wiki/Pony_Express

The name of this package combines the Django mascot (a pony) with a once quite successful mail service in the US.
Ingenious, right?

# Installation

- Install the package via pip:

  `pip install django-pony-express`

  or via pipenv:

  `pipenv install django-pony-express`

- Add module to `INSTALLED_APPS` within the main django `settings.py`:

    ````
    INSTALLED_APPS = (
        ...
        'django_pony_express',
    )
     ````

# Contribute

## Setup package for development

- Create a Python virtualenv and activate it
- Install "pip-tools" with `pip install pip-tools`
- Compile the requirements with `pip-compile --extra dev -o requirements.txt pyproject.toml --resolver=backtracking`
- Sync the dependencies with your virtualenv with `pip-sync`

## Add functionality

- Create a new branch for your feature
- Change the dependency in your requirements.txt to a local (editable) one that points to your local file system:
  `-e /Users/workspace/django-pony-express` or via pip  `pip install -e /Users/workspace/django-pony-express`
- Ensure the code passes the tests
- Create a pull request

## Run tests

- Run tests
  ````
  pytest --ds settings tests
  ````

## Git hooks (via pre-commit)

We use pre-push hooks to ensure that only linted code reaches our remote repository and pipelines aren't triggered in
vain.

To enable the configured pre-push hooks, you need to [install](https://pre-commit.com/) pre-commit and run once:

    pre-commit install -t pre-push -t pre-commit --install-hooks

This will permanently install the git hooks for both, frontend and backend, in your local
[`.git/hooks`](./.git/hooks) folder.
The hooks are configured in the [`.pre-commit-config.yaml`](templates/.pre-commit-config.yaml.tpl).

You can check whether hooks work as intended using the [run](https://pre-commit.com/#pre-commit-run) command:

    pre-commit run [hook-id] [options]

Example: run single hook

    pre-commit run ruff --all-files --hook-stage push

Example: run all hooks of pre-push stage

    pre-commit run --all-files --hook-stage push

## Update documentation

- To build the documentation run: `sphinx-build docs/ docs/_build/html/`.
- Open `docs/_build/html/index.html` to see the documentation.

## Translation files

If you have added custom text, make sure to wrap it in `_()` where `_` is
gettext_lazy (`from django.utils.translation import gettext_lazy as _`).

How to create translation file:

* Navigate to `ai_django_core/ai_django_core` (the inner directory!)
* `python manage.py makemessages -l de`
* Have a look at the new/changed files within `ai_django_core/ai_django_core/locale`

How to compile translation files:

* Navigate to `ai_django_core/ai_django_core` (the inner directory!)
* `python manage.py compilemessages`
* Have a look at the new/changed files within `ai_django_core/ai_django_core/locale`

## Publish to ReadTheDocs.io

- Fetch the latest changes in GitHub mirror and push them
- Trigger new build at ReadTheDocs.io (follow instructions in admin panel at RTD) if the GitHub webhook is not yet set
  up.

## Publish to PyPi

- Update documentation about new/changed functionality

- Update the `Changelog`

- Increment version in main `__init__.py`

- Create pull request / merge to master

- This project uses the flit package to publish to PyPI. Thus publishing should be as easy as running:
  ```
  flit publish
  ```

  To publish to TestPyPI use the following ensure that you have set up your .pypirc as
  shown [here](https://flit.readthedocs.io/en/latest/upload.html#using-pypirc) and use the following command:

  ```
  flit publish --repository testpypi
  ```

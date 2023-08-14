# you find the full pre-commit-tools docu under:
# https://pre-commit.com/

repos:
  - repo: https://github.com/ambv/black
    rev: 23.7.0
    hooks:
      - id: black
        args: [ --check, --diff, --config, ./pyproject.toml ]
        language_version: python3.11
        stages: [ push ]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    # Ruff version.
    rev: 'v0.0.284'
    hooks:
      - id: ruff
        args: [ --fix, --exit-non-zero-on-fix ]

  - repo: https://github.com/asottile/pyupgrade
    rev: v3.10.1
    hooks:
      - id: pyupgrade
        args: [ --py38-plus ]
        language_version: python3.11
        stages: [ push ]

  - repo: https://github.com/adamchainz/django-upgrade
    rev: 1.14.0
    hooks:
      - id: django-upgrade
        args: [--target-version, "3.2"]
        language_version: python3.11
        stages: [ push ]

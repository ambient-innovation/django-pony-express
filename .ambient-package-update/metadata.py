from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import DEV_DEPENDENCIES
from ambient_package_update.metadata.package import PackageMetadata
from ambient_package_update.metadata.ruff_ignored_inspection import RuffIgnoredInspection


METADATA = PackageMetadata(
    package_name='django_pony_express',
    authors=[
        PackageAuthor(
            name='Ambient Digital',
            email='hello@ambient.digital',
        ),
    ],
    development_status='5 - Production/Stable',
    dependencies=[
        'Django>=2.2.28',
        'html2text>=2020.1.16',
    ],
    optional_dependencies={
        'dev': [
            *DEV_DEPENDENCIES,
        ],
    },
    ruff_ignore_list=[
        RuffIgnoredInspection(key='N999', comment="Project name contains underscore, not fixable"),
        RuffIgnoredInspection(key='A003', comment="Django attributes shadow python builtins"),
        RuffIgnoredInspection(key='DJ001', comment="Django model text-based fields shouldn't be nullable"),
        RuffIgnoredInspection(key='B905', comment="Can be enabled when Python <=3.9 support is dropped"),
    ],
)

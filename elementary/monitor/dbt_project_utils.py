import os
from typing import Optional

from elementary.utils.ordered_yaml import OrderedYaml

_MONITOR_DIR = os.path.dirname(os.path.realpath(__file__))

_DBT_PACKAGE_NAME = "elementary"
_DBT_PROJECT_FILENAME = "dbt_project.yml"
_PACKAGES_FILENAME = "packages.yml"

PATH = os.path.join(_MONITOR_DIR, "dbt_project")

# Compatibility for previous dbt versions
_MODULES_PATH = os.path.join(PATH, "dbt_modules")
_PACKAGES_PATH = os.path.join(PATH, "dbt_packages")


def get_elementary_package_path():
    package_path = os.path.join(_PACKAGES_PATH, _DBT_PACKAGE_NAME)
    if os.path.exists(package_path):
        return package_path

    legacy_package_path = os.path.join(_PACKAGES_PATH, _DBT_PACKAGE_NAME)
    if os.path.exists(legacy_package_path):
        return legacy_package_path

    return None


def is_dbt_package_up_to_date() -> bool:
    installed_version = get_installed_dbt_package_version()
    if installed_version is None:
        return False

    required_version = get_required_dbt_package_version()
    return installed_version == required_version


def get_installed_dbt_package_version() -> Optional[str]:
    package_path = get_elementary_package_path()
    if package_path is None:
        return None

    project_path = os.path.join(package_path, _DBT_PROJECT_FILENAME)
    if not os.path.exists(package_path):
        return None

    project_yaml_dict = OrderedYaml().load(project_path)
    return project_yaml_dict["version"]


def get_required_dbt_package_version() -> Optional[str]:
    packages_file_path = os.path.join(PATH, _PACKAGES_FILENAME)
    packages_yaml = OrderedYaml().load(packages_file_path)

    for requirement in packages_yaml["packages"]:
        package_name = requirement["package"].split("/")[-1]
        if package_name == _DBT_PACKAGE_NAME:
            return requirement["version"]

    return None

# SPDX-License-Identifier: LGPL-3.0-or-later
import importlib

from core.version import PROJECT_VERSION


def test_chamanp_package_imports_without_pipeline_side_effects():
    package = importlib.import_module("chamanp")

    assert package.__version__ == PROJECT_VERSION


def test_chamanp_version_export_matches_core_project_version():
    from chamanp import __version__

    assert __version__ == PROJECT_VERSION

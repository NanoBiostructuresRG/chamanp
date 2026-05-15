# SPDX-License-Identifier: LGPL-3.0-or-later
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from chamanp.version import PROJECT_VERSION


def test_chamanp_package_imports_without_pipeline_side_effects():
    package = importlib.import_module("chamanp")

    assert package.__version__ == PROJECT_VERSION


def test_chamanp_version_export_matches_package_project_version():
    from chamanp import __version__

    assert __version__ == PROJECT_VERSION


def test_chamanp_public_api_boundary():
    import chamanp
    from chamanp import ChamanpConfig, ChamanpResult, __version__, run, validate_config

    assert __version__ == chamanp.__version__
    assert chamanp.ChamanpConfig is ChamanpConfig
    assert chamanp.ChamanpResult is ChamanpResult
    assert chamanp.validate_config is validate_config
    assert chamanp.run is run
    assert chamanp.__all__ == [
        "__version__",
        "ChamanpConfig",
        "validate_config",
        "run",
        "ChamanpResult",
    ]
    assert not hasattr(chamanp, "Pipeline")


def test_pipeline_is_not_publicly_importable_from_chamanp():
    with pytest.raises(ImportError):
        from chamanp import Pipeline  # noqa: F401


def test_import_chamanp_in_clean_process_has_no_pipeline_side_effects(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(repo_root)
        if not existing_pythonpath
        else os.pathsep.join([str(repo_root), existing_pythonpath])
    )
    code = """
import json
import sys
import chamanp
from chamanp import ChamanpConfig, ChamanpResult, __version__, run, validate_config

print(json.dumps({
    "version": __version__,
    "has_config": hasattr(chamanp, "ChamanpConfig"),
    "config_name": ChamanpConfig.__name__,
    "has_result": hasattr(chamanp, "ChamanpResult"),
    "result_name": ChamanpResult.__name__,
    "has_validate_config": hasattr(chamanp, "validate_config"),
    "has_run": hasattr(chamanp, "run"),
    "has_pipeline": hasattr(chamanp, "Pipeline"),
    "has_core_attr": hasattr(chamanp, "_core"),
    "has_utils_attr": hasattr(chamanp, "_utils"),
    "base_pipeline_loaded": "chamanp._core.base_pipeline" in sys.modules,
    "public_names": chamanp.__all__,
}))
"""

    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    observed = json.loads(completed.stdout)

    assert observed == {
        "version": PROJECT_VERSION,
        "has_config": True,
        "config_name": "ChamanpConfig",
        "has_result": True,
        "result_name": "ChamanpResult",
        "has_validate_config": True,
        "has_run": True,
        "has_pipeline": False,
        "has_core_attr": False,
        "has_utils_attr": False,
        "base_pipeline_loaded": False,
        "public_names": [
            "__version__",
            "ChamanpConfig",
            "validate_config",
            "run",
            "ChamanpResult",
        ],
    }
    assert not (tmp_path / "artifacts").exists()
    assert not (tmp_path / "artifacts" / "pipeline.log").exists()


def test_private_internal_namespaces_import_without_side_effects(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(repo_root)
        if not existing_pythonpath
        else os.pathsep.join([str(repo_root), existing_pythonpath])
    )
    code = """
import json
import chamanp
import chamanp._core
import chamanp._utils

print(json.dumps({
    "public_api": chamanp.__all__,
    "has_pipeline": hasattr(chamanp, "Pipeline"),
    "core_package": chamanp._core.__name__,
    "utils_package": chamanp._utils.__name__,
}))
"""

    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    observed = json.loads(completed.stdout)

    assert observed == {
        "public_api": [
            "__version__",
            "ChamanpConfig",
            "validate_config",
            "run",
            "ChamanpResult",
        ],
        "has_pipeline": False,
        "core_package": "chamanp._core",
        "utils_package": "chamanp._utils",
    }
    assert not (tmp_path / "artifacts").exists()
    assert not (tmp_path / "artifacts" / "pipeline.log").exists()

# SPDX-License-Identifier: LGPL-3.0-or-later
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import main
from chamanp._core.base_pipeline import Pipeline


def test_main_runs_preflight_before_pipeline(monkeypatch):
    calls = []

    def fake_validate_config(config):
        calls.append(("preflight", config))

    class FakePipeline:
        def __init__(self, config):
            calls.append(("pipeline_init", config))

        def run(self):
            calls.append(("pipeline_run", None))

    monkeypatch.setattr(main, "validate_config", fake_validate_config)
    monkeypatch.setattr(main, "Pipeline", FakePipeline)

    main.main()

    assert [name for name, _ in calls] == [
        "preflight",
        "pipeline_init",
        "pipeline_run",
    ]


def test_importing_base_pipeline_has_no_pipeline_side_effects(tmp_path):
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
import chamanp._core.base_pipeline

print(json.dumps({
    "has_pipeline": hasattr(chamanp._core.base_pipeline, "Pipeline"),
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

    assert observed == {"has_pipeline": True}
    assert not (tmp_path / "artifacts").exists()
    assert not (tmp_path / "artifacts" / "pipeline.log").exists()


def test_pipeline_run_configures_logging_without_real_pipeline_steps(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    calls = []
    config = SimpleNamespace(COLLECTION_TAG="pubchem")
    pipeline = Pipeline(config=config)
    pipeline.filtered_df = []

    monkeypatch.setattr(pipeline, "_create_directories", lambda: calls.append("directories"))
    monkeypatch.setattr(pipeline, "_curate_data", lambda: calls.append("curate"))
    monkeypatch.setattr(pipeline, "_validate_collections", lambda: calls.append("collections"))
    monkeypatch.setattr(pipeline, "_filter_data", lambda: calls.append("filter"))
    monkeypatch.setattr(pipeline, "_generate_fingerprints", lambda: calls.append("fingerprints"))
    monkeypatch.setattr(pipeline, "_write_report", lambda: calls.append("report"))

    pipeline.run()

    assert calls == [
        "directories",
        "curate",
        "collections",
        "filter",
        "fingerprints",
        "report",
    ]
    assert (tmp_path / "artifacts").is_dir()
    assert (tmp_path / "artifacts" / "pipeline.log").is_file()

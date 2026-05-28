# SPDX-License-Identifier: LGPL-3.0-or-later
import os
import subprocess
import sys
from pathlib import Path

from chamanp import ChamanpResult, __version__
from chamanp import cli


def run_module_command(module, *args, cwd):
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(repo_root)
        if not existing_pythonpath
        else os.pathsep.join([str(repo_root), existing_pythonpath])
    )
    return subprocess.run(
        [sys.executable, "-m", module, *args],
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def write_valid_profile(tmp_path):
    database_path = tmp_path / "input.csv"
    taxonomy_path = tmp_path / "taxonomy.json"
    profile_path = tmp_path / "chamanp.toml"
    database_path.write_text("identifier,canonical_smiles\n", encoding="utf-8")
    taxonomy_path.write_text('{"entries": ["PubChem NPs"]}', encoding="utf-8")
    profile_path.write_text(
        "\n".join(
            [
                f'database_path = "{database_path.as_posix()}"',
                f'collection_taxonomy_path = "{taxonomy_path.as_posix()}"',
                'target_collections = ["PubChem NPs"]',
                'collection_tag = "cli_test"',
                'collection_logic = "OR"',
            ]
        ),
        encoding="utf-8",
    )
    return profile_path


def test_cli_version(capsys):
    try:
        cli.main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0

    captured = capsys.readouterr()
    assert captured.out.strip() == __version__


def test_package_module_version(tmp_path):
    completed = run_module_command("chamanp", "--version", cwd=tmp_path)

    assert completed.returncode == 0
    assert completed.stdout.strip() == __version__
    assert completed.stderr == ""


def test_package_module_help(tmp_path):
    completed = run_module_command("chamanp", "--help", cwd=tmp_path)

    assert completed.returncode == 0
    assert "usage: chamanp" in completed.stdout
    assert "check-config" in completed.stdout
    assert "run" in completed.stdout
    assert completed.stderr == ""


def test_cli_module_version(tmp_path):
    completed = run_module_command("chamanp.cli", "--version", cwd=tmp_path)

    assert completed.returncode == 0
    assert completed.stdout.strip() == __version__
    assert completed.stderr == ""


def test_cli_check_config_success(tmp_path, capsys):
    profile_path = write_valid_profile(tmp_path)

    exit_code = cli.main(["check-config", str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert f"Configuration OK: {profile_path}" in captured.out
    assert captured.err == ""
    assert not (tmp_path / "artifacts").exists()


def test_cli_check_config_missing_file_fails_cleanly(tmp_path, capsys):
    profile_path = tmp_path / "missing.toml"

    exit_code = cli.main(["check-config", str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error:" in captured.err
    assert "TOML configuration file not found" in captured.err
    assert "Traceback" not in captured.err
    assert "Traceback" not in captured.out


def test_cli_check_config_malformed_toml_fails_cleanly(tmp_path, capsys):
    profile_path = tmp_path / "broken.toml"
    profile_path.write_text("collection_tag = [\n", encoding="utf-8")

    exit_code = cli.main(["check-config", str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error:" in captured.err
    assert "Malformed TOML configuration file" in captured.err
    assert "Traceback" not in captured.err
    assert "Traceback" not in captured.out


def test_cli_run_success_uses_public_api_without_real_pipeline(tmp_path, monkeypatch, capsys):
    profile_path = write_valid_profile(tmp_path)
    calls = []
    expected_result = ChamanpResult(
        status="completed",
        version="test",
        collection_tag="cli_test",
        curated_path="artifacts/curated_cli_test.csv",
        filtered_path="artifacts/filtered_cli_test.csv",
        metadata_path="artifacts/valid_metadata_cli_test.csv",
        fingerprints_path="artifacts/X_cli_test.npy",
        invalid_smiles_path="artifacts/invalid_smiles_cli_test.csv",
        report_path="artifacts/reports/report_dbprep_cli_test.txt",
        fingerprint_radius=2,
        fingerprint_bits=1024,
    )

    def fake_run(config):
        calls.append(config)
        return expected_result

    monkeypatch.setattr(cli, "run", fake_run)

    exit_code = cli.main(["run", str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert len(calls) == 1
    assert "CHAMANP run completed." in captured.out
    assert "Status: completed" in captured.out
    assert "Output directory: artifacts" in captured.out
    assert captured.err == ""


def test_cli_run_failure_fails_cleanly(tmp_path, monkeypatch, capsys):
    profile_path = write_valid_profile(tmp_path)

    def fake_run(config):
        raise RuntimeError("pipeline failed")

    monkeypatch.setattr(cli, "run", fake_run)

    exit_code = cli.main(["run", str(profile_path)])

    captured = capsys.readouterr()
    assert exit_code != 0
    assert "Error: pipeline failed" in captured.err
    assert "Traceback" not in captured.err
    assert "Traceback" not in captured.out

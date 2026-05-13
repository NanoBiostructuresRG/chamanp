from core.version import PROJECT_NAME, PROJECT_STATUS, PROJECT_VERSION
from utils.result_manager import ResultManager


def test_report_header_uses_centralized_project_metadata(tmp_path):
    manager = ResultManager(tmp_path / "report.txt")

    header = manager._get_header()

    assert PROJECT_NAME in header
    assert f"Version: {PROJECT_VERSION}" in header
    assert f"Status: {PROJECT_STATUS}" in header
    assert "Execution Date:" in header


def test_report_header_does_not_use_legacy_v1_version():
    manager = ResultManager("report.txt")

    header = manager._get_header()

    assert "v1.0" not in header
    assert "May, 2025. Oviedo" not in header

"""Logging configuration tests."""

from pathlib import Path

from verse_agent.core.config import LoggingSettings
from verse_agent.core.logging import _log_file_path


def test_log_file_path_uses_current_working_directory_for_relative_paths(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)

    log_path = _log_file_path(LoggingSettings(directory="logs", file_name="verse-agent.log"))

    assert log_path == tmp_path / "logs" / "verse-agent.log"
    assert log_path.parent.exists()

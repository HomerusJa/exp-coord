from pathlib import Path

import pytest

from exp_coord.core.config import find_file


def test_find_file_in_current_directory(tmp_path, mocker):
    test_file = tmp_path / "test.txt"
    test_file.touch()

    mocker.patch("exp_coord.core.config.__file__", str(tmp_path / "your_module.py"))
    result = find_file("test.txt")
    assert result == test_file


def test_find_file_in_parent_directory(tmp_path):
    parent_dir = tmp_path / "parent"
    child_dir = parent_dir / "child"
    parent_dir.mkdir()
    child_dir.mkdir()

    test_file = parent_dir / "test.txt"
    test_file.touch()

    result = find_file("test.txt", base_path=child_dir)
    assert result == test_file


def test_mount_point_behavior(tmp_path, mocker):
    mocker.patch.object(Path, "is_mount", return_value=True)

    with pytest.raises(FileNotFoundError):
        find_file("test.txt", base_path=tmp_path)

# tests/actions/test_find_duplicate_files.py

import os
import pytest
from unittest.mock import patch
from pro_filer.actions.main_actions import find_duplicate_files


@pytest.fixture
def tmp_files(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Hello, World!")

    file2 = tmp_path / "file2.txt"
    file2.write_text("Test file content")

    return [str(file1), str(file2)]


def test_find_duplicate_files_no_duplicates(tmp_files):
    context = {"all_files": tmp_files}
    result = find_duplicate_files(context)
    assert result == []


def test_find_duplicate_files_with_duplicates(tmp_files):
    duplicate_file = tmp_files[0] + "_duplicate"
    os.link(tmp_files[0], duplicate_file)

    context = {"all_files": tmp_files + [duplicate_file]}
    result = find_duplicate_files(context)

    expected_result = [(tmp_files[0], duplicate_file)]
    assert result == expected_result


def test_find_duplicate_files_missing_file(tmp_files):
    missing_file = tmp_files[0]

    context = {"all_files": tmp_files}

    with patch(
        "pro_filer.actions.main_actions.filecmp.cmp",
        side_effect=FileNotFoundError(f"File not found: {missing_file}"),
    ):
        with pytest.raises(ValueError, match="All files must exist"):
            find_duplicate_files(context)

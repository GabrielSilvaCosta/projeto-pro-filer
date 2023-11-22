from unittest.mock import patch, MagicMock
from pro_filer.actions.main_actions import show_details


def test_show_details_existing_file(capsys):
    context = {"base_path": "/home/trybe/Downloads/Trybe_logo.png"}

    with patch(
        "pro_filer.actions.main_actions.os.path.exists", return_value=True
    ), patch(
        "pro_filer.actions.main_actions.os.stat",
        return_value=MagicMock(st_size=22438, st_mtime=1676267118),
    ), patch(
        "pro_filer.actions.main_actions.os.path.isdir", return_value=False
    ):
        show_details(context)
        captured = capsys.readouterr()

    assert (
        captured.out == "File name: Trybe_logo.png\n"
        "File size in bytes: 22438\n"
        "File type: file\n"
        "File extension: .png\n"
        "Last modified date: 2023-02-13\n"
    )


def test_show_details_non_existing_file(capsys):
    context = {"base_path": "/path/to/non_existing_file"}

    with patch(
        "pro_filer.actions.main_actions.os.path.exists", return_value=False
    ):
        show_details(context)
        captured = capsys.readouterr()

    assert captured.out == "File 'non_existing_file' does not exist\n"


def test_show_details_non_existing_dir(capsys):
    context = {"base_path": "/path/to/non_existing_dir"}

    with patch(
        "pro_filer.actions.main_actions.os.path.exists", return_value=False
    ):
        show_details(context)
        captured = capsys.readouterr()

    assert captured.out == "File 'non_existing_dir' does not exist\n"


def test_show_details_custom_failure(capsys):
    context = {"base_path": "fake_file"}

    with patch(
        "pro_filer.actions.main_actions.os.path.exists", return_value=False
    ):
        show_details(context)

    captured = capsys.readouterr()
    assert captured.out == f"File '{context['base_path']}' does not exist\n"


def test_show_details_file_without_extension(capsys):
    context = {"base_path": "/path/to/file_without_extension"}

    with patch(
        "pro_filer.actions.main_actions.os.path.exists", return_value=True
    ), patch(
        "pro_filer.actions.main_actions.os.path.isdir", return_value=False
    ), patch(
        "pro_filer.actions.main_actions.os.path.splitext",
        return_value=("/path/to/file_without_extension", ""),
    ), patch(
        "pro_filer.actions.main_actions.os.stat",
        return_value=MagicMock(st_size=12345, st_mtime=1676267118),
    ):
        show_details(context)
        captured = capsys.readouterr()

    assert (
        captured.out == "File name: file_without_extension\n"
        "File size in bytes: 12345\n"
        "File type: file\n"
        "File extension: [no extension]\n"
        "Last modified date: 2023-02-13\n"
    )

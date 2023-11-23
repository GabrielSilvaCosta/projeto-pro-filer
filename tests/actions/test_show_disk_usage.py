from pro_filer.actions.main_actions import show_disk_usage  # NOQA


def test_empty_file(capsys):
    assert "Total size: 0" in capture_output({"all_files": []}, capsys)


def test_show_disk_usage(tmp_path, capsys):
    create_test_files(tmp_path)
    assert "Total size: 2849" in capture_output(
        get_fake_context(tmp_path), capsys
    )


def test_sorted_output(tmp_path, capsys):
    create_test_files(tmp_path)
    captured = capture_output(get_fake_context(tmp_path), capsys)
    assert is_output_sorted_by_size(captured) and "Total size:" in captured


def create_test_files(tmp_path):
    src_path = tmp_path / "src"
    src_path.mkdir()
    (src_path / "app.py").write_text("a" * 2849)
    (src_path / "__init__.py").write_text("")


def get_fake_context(tmp_path):
    src_path = tmp_path / "src"
    return {
        "all_files": [str(src_path / "app.py"), str(src_path / "__init__.py")]
    }


def capture_output(context, capsys):
    show_disk_usage(context)
    return capsys.readouterr().out


def is_output_sorted_by_size(captured_output):
    file_info = [
        (
            line.split(":")[0].strip("'").strip(),
            int(line.split(":")[1].split("(")[0].strip()),
        )
        for line in [
            la for la in captured_output.split("\n") if la.startswith("'")
        ]
    ]
    return file_info == sorted(file_info, key=lambda x: x[1], reverse=True)

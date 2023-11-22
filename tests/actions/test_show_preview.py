from pro_filer.actions.main_actions import show_preview


def test_show_preview_with_data(capfd):
    context = {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
        ],
        "all_dirs": ["src", "src/utils"],
    }

    show_preview(context)

    out, _ = capfd.readouterr()
    expected_output = (
        "Found 3 files and 2 directories\n"
        f"First 5 files: {context['all_files'][:5]}\n"
        f"First 5 directories: {context['all_dirs'][:5]}\n"
    )

    assert out == expected_output


def test_show_preview_with_empty_data(capfd):
    context = {"all_files": [], "all_dirs": []}

    show_preview(context)

    out, _ = capfd.readouterr()
    expected_output = "Found 0 files and 0 directories\n"
    assert out == expected_output

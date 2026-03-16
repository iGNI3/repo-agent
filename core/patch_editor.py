import difflib


def create_patch(old_text, new_text):

    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        lineterm=""
    )

    return "\n".join(diff)


def apply_patch(file_path, new_content):

    with open(file_path, "w") as f:
        f.write(new_content)
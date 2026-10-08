import sys


def get_command(source_file: str) -> list[str]:
    """
    Return the command required to execute a Python submission.
    """

    return [
        sys.executable,
        source_file
    ]
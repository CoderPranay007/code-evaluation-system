def normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def compare_output(actual: str, expected: str) -> bool:
    return normalize_output(actual) == normalize_output(expected)
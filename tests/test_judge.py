from judge.judge import evaluate
from judge.verdict import AC, WA, RE, TLE


def test_accepted():
    source_code = """
print("Hello World")
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="",
        expected_output="Hello World\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == AC
    print("AC test: PASS")


def test_wrong_answer():
    source_code = """
print("Wrong Answer")
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="",
        expected_output="Correct Answer\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == WA
    print("WA test: PASS")


def test_runtime_error():
    source_code = """
print(10 / 0)
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="",
        expected_output="",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == RE
    print("RE test: PASS")


def test_time_limit():
    source_code = """
while True:
    pass
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="",
        expected_output="",
        time_limit=500,
        memory_limit=64
    )

    assert result.verdict == TLE
    print("TLE test: PASS")


if __name__ == "__main__":
    test_accepted()
    test_wrong_answer()
    test_runtime_error()
    test_time_limit()

    print()
    print("All Step 1 tests passed.")
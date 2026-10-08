from judge.judge import evaluate
from judge.verdict import AC, WA, RE, TLE, CE

def test_python_accepted():

    source_code = """
n = int(input())
print(n * 2)
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="5\n",
        expected_output="10\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == AC

    print("Python AC test: PASS")


def test_python_wrong_answer():

    source_code = """
n = int(input())
print(n * 3)
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="5\n",
        expected_output="10\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == WA

    print("Python WA test: PASS")


def test_python_runtime_error():

    source_code = """
n = int(input())
print(n / 0)
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="5\n",
        expected_output="10\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == RE

    print("Python RE test: PASS")


def test_python_time_limit():

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

    print("Python TLE test: PASS")



def test_cpp_accepted():

    source_code = r"""
#include <iostream>

using namespace std;

int main() {

    int n;
    cin >> n;

    cout << n * 2 << endl;

    return 0;
}
"""

    result = evaluate(
        source_code=source_code,
        language="cpp",
        input_data="5\n",
        expected_output="10\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == AC

    print("C++ AC test: PASS")


def test_cpp_wrong_answer():

    source_code = r"""
#include <iostream>

using namespace std;

int main() {

    int n;
    cin >> n;

    cout << n * 3 << endl;

    return 0;
}
"""

    result = evaluate(
        source_code=source_code,
        language="cpp",
        input_data="5\n",
        expected_output="10\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == WA

    print("C++ WA test: PASS")


def test_cpp_runtime_error():

    source_code = r"""
#include <iostream>

using namespace std;

int main() {

    return 1;
}
"""

    result = evaluate(
        source_code=source_code,
        language="cpp",
        input_data="",
        expected_output="",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == RE

    print("C++ RE test: PASS")


def test_cpp_compilation_error():

    source_code = r"""
#include <iostream>

using namespace std;

int main() {

    cout << "Hello World" << endl

    return 0;
}
"""

    result = evaluate(
        source_code=source_code,
        language="cpp",
        input_data="",
        expected_output="Hello World\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == CE

    print("C++ CE test: PASS")


def test_evaluate_single_test_case():
    source_code = """
n = int(input())
print(n * 2)
"""

    result = evaluate(
        source_code=source_code,
        language="python",
        input_data="21\n",
        expected_output="42\n",
        time_limit=1000,
        memory_limit=64
    )

    assert result.verdict == AC
    assert result.actual_output == "42\n"
    assert result.execution_time is not None
    assert result.memory_used is not None

    print(f"Memory used: {result.memory_used} KB")

    print("Single test-case evaluation: PASS")


if __name__ == "__main__":
    test_python_accepted()
    test_python_wrong_answer()
    test_python_runtime_error()
    test_python_time_limit()
    test_cpp_accepted()
    test_cpp_wrong_answer()
    test_cpp_runtime_error()
    test_cpp_compilation_error()
    test_evaluate_single_test_case()

    print()
    print("All Step 5 tests passed.")
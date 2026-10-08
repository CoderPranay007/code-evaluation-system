from judge.sandbox.docker_cpp import run_cpp_in_docker
from judge.executor import ExecutionResult


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


result = run_cpp_in_docker(
    source_code=source_code,
    input_data="5\n",
    timeout_seconds=5
)


print("STDOUT:")
print(result.stdout)

print("STDERR:")
print(result.stderr)

print("RETURN CODE:")
print(result.return_code)

print("TIMED OUT:")
print(result.timed_out)


assert isinstance(result, ExecutionResult)
assert result.return_code == 0
assert result.stdout == "10\n"
assert result.timed_out is False
assert result.execution_time_ms > 0

print(f"Execution time: {result.execution_time_ms:.2f} ms")

print("Docker C++ structured result test: PASS")

print()
print("Testing C++ TLE...")

tle_source_code = r"""
#include <iostream>
using namespace std;

int main() {
    while (true) {
    }

    return 0;
}
"""

tle_result = run_cpp_in_docker(
    source_code=tle_source_code,
    input_data="",
    timeout_seconds=2
)

print("TLE RETURN CODE:")
print(tle_result.return_code)

print("TLE TIMED OUT:")
print(tle_result.timed_out)

print("TLE EXECUTION TIME:")
print(tle_result.execution_time_ms)

assert tle_result.timed_out is True
assert tle_result.return_code is None
assert tle_result.execution_time_ms >= 2000

print("Docker C++ TLE test: PASS")
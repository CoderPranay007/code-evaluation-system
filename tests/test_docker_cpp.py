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
print()

print("Testing C++ memory limit...")

memory_source_code = r"""
#include <vector>
#include <iostream>

int main() {
    const size_t size = 512ULL * 1024 * 1024;

    volatile char* data = new char[size];

    for (size_t i = 0; i < size; i += 4096) {
        data[i] = 1;
    }

    std::cout << "allocated" << std::endl;

    delete[] data;

    return 0;
}
"""

memory_result = run_cpp_in_docker(
    source_code=memory_source_code,
    input_data="",
    timeout_seconds=10,
    memory_limit_mb=256
)

print("MLE RETURN CODE:")
print(memory_result.return_code)

print("MLE TIMED OUT:")
print(memory_result.timed_out)

print("MLE STDERR:")
print(memory_result.stderr)

print("MLE EXECUTION TIME:")
print(memory_result.execution_time_ms)

assert memory_result.memory_limit_exceeded is True
assert memory_result.timed_out is False

print("Docker C++ MLE test: PASS")
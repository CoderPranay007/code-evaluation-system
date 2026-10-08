from judge.sandbox.docker_python import run_python_in_docker
from judge.executor import ExecutionResult


source_code = """
n = int(input())
print(n * 2)
"""


result = run_python_in_docker(
    source_code=source_code,
    input_data="5\n",
    timeout_seconds=10
)


print("STDOUT:")
print(result.stdout)

print("STDERR:")
print(result.stderr)

print("RETURN CODE:")
print(result.return_code)

print("TIMED OUT:")
print(result.timed_out)

print("EXECUTION TIME:")
print(result.execution_time_ms)


assert isinstance(result, ExecutionResult)
assert result.return_code == 0
assert result.stdout == "10\n"
assert result.timed_out is False
assert result.execution_time_ms > 0

print("Docker Python test: PASS")
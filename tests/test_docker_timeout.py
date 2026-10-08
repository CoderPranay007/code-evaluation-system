from judge.sandbox.docker_runner import run_docker_container


result = run_docker_container(
    image="gcc:latest",
    container_command=[
        "bash",
        "-c",
        "while true; do :; done"
    ],
    input_data="",
    timeout_seconds=2
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


assert result.timed_out is True
assert result.return_code is None
assert result.execution_time_ms >= 2000

print("Docker TLE test: PASS")
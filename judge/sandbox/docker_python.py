import os
import tempfile

from judge.sandbox.docker_runner import run_docker_container
from judge.executor import ExecutionResult


def run_python_in_docker(
    source_code: str,
    input_data: str,
    timeout_seconds: float,
    memory_limit_mb: int | None = None
) -> ExecutionResult:

    with tempfile.TemporaryDirectory(
        prefix="judge_python_"
    ) as temp_dir:

        source_file = os.path.join(
            temp_dir,
            "main.py"
        )

        with open(
            source_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(source_code)

        return run_docker_container(
            image="python:3.13",
            container_command=[
                "python",
                "/workspace/main.py"
            ],
            input_data=input_data,
            timeout_seconds=timeout_seconds,
            memory_limit_mb=memory_limit_mb,
            volume_mount=f"{temp_dir}:/workspace"
        )
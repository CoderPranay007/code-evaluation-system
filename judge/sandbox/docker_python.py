import os
import subprocess
import tempfile
import time

from judge.executor import ExecutionResult


def run_python_in_docker(
    source_code: str,
    input_data: str,
    timeout_seconds: float
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

        command = [
            "docker",
            "run",
            "--rm",
            "-i",
            "-v",
            f"{temp_dir}:/workspace",
            "python:3.13",
            "python",
            "/workspace/main.py"
        ]

        start_time = time.perf_counter()

        try:

            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )

            end_time = time.perf_counter()

            return ExecutionResult(
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                execution_time_ms=(
                    end_time - start_time
                ) * 1000,
                timed_out=False,
                memory_used_kb=None
            )

        except subprocess.TimeoutExpired as exc:

            end_time = time.perf_counter()

            return ExecutionResult(
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                return_code=None,
                execution_time_ms=(
                    end_time - start_time
                ) * 1000,
                timed_out=True,
                memory_used_kb=None
            )
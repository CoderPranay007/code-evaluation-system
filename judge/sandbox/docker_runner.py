import subprocess
import time
import uuid

from judge.executor import ExecutionResult


def run_docker_container(
    image: str,
    container_command: list[str],
    input_data: str,
    timeout_seconds: float,
    memory_limit_mb: int | None = None,
    volume_mount: str | None = None
) -> ExecutionResult:

    container_name = f"judge_{uuid.uuid4().hex[:12]}"

    command = [
        "docker",
        "run",
        "--name",
        container_name,
        "-i",
    ]

    if memory_limit_mb is not None:
        command += [
            "--memory",
            f"{memory_limit_mb}m"
        ]

    if volume_mount is not None:
        command.extend([
            "-v",
            volume_mount
        ])

    command.extend([
        image,
        *container_command
    ])

    start_time = time.perf_counter()

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:

        stdout, stderr = process.communicate(
            input=input_data,
            timeout=timeout_seconds
        )

        oom_killed = False

        inspect_result = subprocess.run(
            [
                "docker",
                "inspect",
                "--format",
                "{{.State.OOMKilled}}",
                container_name
            ],
            capture_output=True,
            text=True
        )
        
        if inspect_result.returncode == 0:
            oom_killed = inspect_result.stdout.strip().lower() == "true"
        
        subprocess.run(
            [
                "docker",
                "rm",
                "-f",
                container_name
            ],
            capture_output=True,
            text=True
        )

        end_time = time.perf_counter()

        return ExecutionResult(
            stdout=stdout,
            stderr=stderr,
            return_code=process.returncode,
            execution_time_ms=(
                end_time - start_time
            ) * 1000,
            timed_out=False,
            memory_used_kb=None,
            memory_limit_exceeded=oom_killed
        )

    except subprocess.TimeoutExpired:

        # Kill the actual Docker container
        subprocess.run(
            [
                "docker",
                "kill",
                container_name
            ],
            capture_output=True,
            text=True
        )

        # Make sure the Docker CLI process finishes
        try:
            stdout, stderr = process.communicate(
                timeout=5
            )
        except subprocess.TimeoutExpired:

            process.kill()

            stdout, stderr = process.communicate()

        # Cleanup in case --rm did not remove it
        subprocess.run(
            [
                "docker",
                "rm",
                "-f",
                container_name
            ],
            capture_output=True,
            text=True
        )

        end_time = time.perf_counter()

        return ExecutionResult(
            stdout=stdout or "",
            stderr=stderr or "",
            return_code=None,
            execution_time_ms=(
                end_time - start_time
            ) * 1000,
            timed_out=True,
            memory_used_kb=None,
            memory_limit_exceeded=False
        )
import os
import tempfile

from judge.sandbox.docker_runner import run_docker_container
from judge.executor import ExecutionResult


def run_cpp_in_docker(
    source_code: str,
    input_data: str,
    timeout_seconds: float,
    memory_limit_mb: int | None = None
) -> ExecutionResult:

    with tempfile.TemporaryDirectory(
        prefix="judge_cpp_"
    ) as temp_dir:

        source_file = os.path.join(
            temp_dir,
            "main.cpp"
        )

        with open(
            source_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(source_code)


        # Step 1: Compile

        compile_result = run_docker_container(
            image="gcc:latest",
            container_command=[
                "g++",
                "/workspace/main.cpp",
                "-std=c++17",
                "-O2",
                "-o",
                "/workspace/main"
            ],
            input_data="",
            timeout_seconds=30,
            memory_limit_mb=None,
            volume_mount=f"{temp_dir}:/workspace"
        )

        if compile_result.timed_out:

            compile_result.compilation_failed = True
            return compile_result

        if compile_result.return_code != 0:

            compile_result.compilation_failed = True
            return compile_result

        # Step 2: Execute
    
        execution_result = run_docker_container(
            image="gcc:latest",
            container_command=[
                "/workspace/main"
            ],
            input_data=input_data,
            timeout_seconds=timeout_seconds,
            memory_limit_mb=memory_limit_mb,
            volume_mount=f"{temp_dir}:/workspace"
        )

        return execution_result
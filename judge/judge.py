from dataclasses import dataclass
import os
import tempfile

from judge.executor import run_process, is_execution_successful
from judge.comparator import compare_output
from judge.verdict import AC, WA, CE, RE, TLE
from judge.compiler.python import get_command
from judge.compiler.cpp import compile_cpp


@dataclass
class JudgeResult:

    verdict: str

    execution_time: float | None = None
    memory_used: int | None = None
    actual_output: str | None = None
    error_message: str | None = None


def evaluate(
    source_code: str,
    language: str,
    input_data: str,
    expected_output: str,
    time_limit: int,
    memory_limit: int
) -> JudgeResult:

    language = language.lower().strip()

    if language == "py":
        language = "python"

    if language in {"c++", "cc", "cxx"}:
        language = "cpp"

    with tempfile.TemporaryDirectory(
        prefix="judge_"
    ) as temp_dir:

        source_file = None
        executable_file = None


        if language == "python":

            source_file = os.path.join(
                temp_dir,
                "submission.py"
            )

            with open(
                source_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(source_code)

            command = get_command(source_file)


        elif language == "cpp":

            source_file = os.path.join(
                temp_dir,
                "submission.cpp"
            )

            executable_file = os.path.join(
                temp_dir,
                "submission.exe"
            )

            with open(
                source_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(source_code)

            compilation = compile_cpp(
                source_file=source_file,
                executable_file=executable_file
            )

            if compilation.timed_out:

                return JudgeResult(
                    verdict=CE,
                    error_message="Compilation timed out"
                )

            if not compilation.success:

                return JudgeResult(
                    verdict=CE,
                    error_message=compilation.stderr
                )

            command = [executable_file]

        else:

            return JudgeResult(
                verdict=RE,
                error_message=f"Unsupported language: {language}"
            )

        # EXECUTION

        timeout_seconds = time_limit / 1000

        result = run_process(
            command=command,
            input_data=input_data,
            timeout_seconds=timeout_seconds
        )

        actual_output = result.stdout

        if result.timed_out:

            return JudgeResult(
                verdict=TLE,
                execution_time=result.execution_time_ms,
                memory_used=result.memory_used_kb,
                actual_output=actual_output,
                error_message="Time limit exceeded"
            )


        if not is_execution_successful(result):

            return JudgeResult(
                verdict=RE,
                execution_time=result.execution_time_ms,
                memory_used=result.memory_used_kb,
                actual_output=actual_output,
                error_message=result.stderr
            )

        if compare_output(
            actual_output,
            expected_output
        ):

            return JudgeResult(
                verdict=AC,
                execution_time=result.execution_time_ms,
                memory_used=result.memory_used_kb,
                actual_output=actual_output,
                error_message=None
            )


        return JudgeResult(
            verdict=WA,
            execution_time=result.execution_time_ms,
            memory_used=result.memory_used_kb,
            actual_output=actual_output,
            error_message=None
        )
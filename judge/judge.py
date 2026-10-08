from dataclasses import dataclass

from judge.executor import is_execution_successful
from judge.comparator import compare_output
from judge.verdict import AC, WA, CE, RE, TLE, MLE
from judge.sandbox.docker_python import run_python_in_docker
from judge.sandbox.docker_cpp import run_cpp_in_docker


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

    # EXECUTION
    
    if language == "python":

        result = run_python_in_docker(
            source_code=source_code,
            input_data=input_data,
            timeout_seconds=time_limit / 1000,
            memory_limit_mb=memory_limit
        )

    elif language == "cpp":

        result = run_cpp_in_docker(
            source_code=source_code,
            input_data=input_data,
            timeout_seconds=time_limit / 1000,
            memory_limit_mb=memory_limit
        )

    else:

        return JudgeResult(
            verdict=RE,
            error_message=f"Unsupported language: {language}"
        )

    actual_output = result.stdout

    if result.compilation_failed:

        return JudgeResult(
            verdict=CE,
            execution_time=result.execution_time_ms,
            memory_used=result.memory_used_kb,
            actual_output=actual_output,
            error_message=result.stderr
        )
    
    if result.timed_out:

        return JudgeResult(
            verdict=TLE,
            execution_time=result.execution_time_ms,
            memory_used=result.memory_used_kb,
            actual_output=actual_output,
            error_message="Time limit exceeded"
        )
    
    if result.memory_limit_exceeded:

        return JudgeResult(
            verdict=MLE,
            execution_time=result.execution_time_ms,
            memory_used=result.memory_used_kb,
            actual_output=actual_output,
            error_message="Memory limit exceeded"
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
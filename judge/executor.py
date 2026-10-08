from dataclasses import dataclass
import subprocess
import time


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    return_code: int | None
    execution_time_ms: float
    timed_out: bool


def _decode_output(output):
    if output is None:
        return ""

    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")

    return output


def run_process(
    command: list[str],
    input_data: str,
    timeout_seconds: float
) -> ExecutionResult:

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
            execution_time_ms=(end_time - start_time) * 1000,
            timed_out=False
        )

    except subprocess.TimeoutExpired as exc:

        end_time = time.perf_counter()

        return ExecutionResult(
            stdout=_decode_output(exc.stdout),
            stderr=_decode_output(exc.stderr),
            return_code=None,
            execution_time_ms=(end_time - start_time) * 1000,
            timed_out=True
        )

def is_execution_successful(result: ExecutionResult) -> bool:
    return (
        not result.timed_out
        and result.return_code == 0
    )
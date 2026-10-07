import subprocess
import time


def _decode_output(output):
    """
    Convert subprocess output into a string.

    Normally subprocess.run() gives us a string because
    text=True is used. TimeoutExpired can sometimes contain
    bytes, so we handle both cases.
    """

    if output is None:
        return ""

    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")

    return output


def run_process(command, input_data: str, timeout_seconds: float) -> dict:
    """
    Execute a process.

    Returns:
        stdout
        stderr
        return_code
        execution_time_ms
        timed_out
    """

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

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "execution_time_ms": (end_time - start_time) * 1000,
            "timed_out": False
        }

    except subprocess.TimeoutExpired as exc:
        end_time = time.perf_counter()

        return {
            "stdout": _decode_output(exc.stdout),
            "stderr": _decode_output(exc.stderr),
            "return_code": None,
            "execution_time_ms": (end_time - start_time) * 1000,
            "timed_out": True
        }
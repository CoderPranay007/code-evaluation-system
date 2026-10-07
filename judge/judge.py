from dataclasses import dataclass
import os
import sys
import tempfile

from judge.executor import run_process
from judge.comparator import compare_output
from judge.verdict import AC, WA, RE, TLE


@dataclass
class JudgeResult:
    """ Result returned by the Judge."""

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
    """
    Evaluate one submitted program against one test case.

    Parameters:
        source_code:
            Complete submitted source code.

        language:
            Currently supported:
                python

    """

    language = language.lower().strip()

    # ---------------------------------------------------------
    # Currently only Python is supported.
    # ---------------------------------------------------------

    if language not in {"python", "py"}:
        return JudgeResult(
            verdict=RE,
            error_message=f"Unsupported language: {language}"
        )

    # ---------------------------------------------------------
    # Convert milliseconds to seconds because subprocess.run()
    # expects timeout in seconds.
    # ---------------------------------------------------------

    timeout_seconds = time_limit / 1000

    temp_file_path = None

    try:
        # -----------------------------------------------------
        # Create a temporary Python source file.
        # -----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as temp_file:

            temp_file.write(source_code)
            temp_file_path = temp_file.name

        # -----------------------------------------------------
        # Execute the submitted Python program.
        # -----------------------------------------------------

        result = run_process(
            [sys.executable, temp_file_path],
            input_data,
            timeout_seconds
        )

        actual_output = result["stdout"]

        if result["timed_out"]:
            return JudgeResult(
                verdict=TLE,
                execution_time=result["execution_time_ms"],
                memory_used=None,
                actual_output=actual_output,
                error_message="Time limit exceeded"
            )


        if result["return_code"] != 0:
            return JudgeResult(
                verdict=RE,
                execution_time=result["execution_time_ms"],
                memory_used=None,
                actual_output=actual_output,
                error_message=result["stderr"]
            )


        if compare_output(
            actual_output,
            expected_output
        ):
            verdict = AC
        else:
            verdict = WA

        return JudgeResult(
            verdict=verdict,
            execution_time=result["execution_time_ms"],
            memory_used=None,
            actual_output=actual_output,
            error_message=None
        )

    except Exception as exc:
        # -----------------------------------------------------
        # Internal judge error.
        #
        # We don't have IE in the current return structure yet,
        # so represent unexpected judge failure as RE for now.
        # We will improve this later.
        # -----------------------------------------------------

        return JudgeResult(
            verdict=RE,
            error_message=f"Judge error: {exc}"
        )

    finally:
        # -----------------------------------------------------
        # Always remove the temporary source file.
        # -----------------------------------------------------

        if temp_file_path is not None:
            try:
                os.remove(temp_file_path)
            except OSError:
                pass
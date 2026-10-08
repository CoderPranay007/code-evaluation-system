import subprocess

from judge.compiler.base import CompilationResult


def compile_cpp(
    source_file: str,
    executable_file: str,
    timeout_seconds: float = 5.0
) -> CompilationResult:

    command = [
        "g++",
        source_file,
        "-std=c++17",
        "-O2",
        "-o",
        executable_file
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        return CompilationResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
            timed_out=False
        )

    except subprocess.TimeoutExpired as exc:

        stderr = exc.stderr

        if isinstance(stderr, bytes):
            stderr = stderr.decode(
                "utf-8",
                errors="replace"
            )

        return CompilationResult(
            success=False,
            stdout="",
            stderr=stderr or "",
            return_code=None,
            timed_out=True
        )
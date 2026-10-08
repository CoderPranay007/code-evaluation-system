import subprocess

def compile_cpp(
    source_file: str,
    executable_file: str,
    timeout_seconds: float = 5.0
) -> dict:
    """
    Compile a C++ source file using g++.

    Parameters:
        source_file:
            Path to the submitted .cpp file.

        executable_file:
            Path where the compiled executable should be created.

        timeout_seconds:
            Maximum time allowed for compilation.

    Returns:
        {
            "success": bool,
            "stderr": str,
            "stdout": str,
            "return_code": int | None,
            "timed_out": bool
        }
    """

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

        return {
            "success": result.returncode == 0,
            "stderr": result.stderr,
            "stdout": result.stdout,
            "return_code": result.returncode,
            "timed_out": False
        }

    except subprocess.TimeoutExpired as exc:

        stderr = exc.stderr

        if isinstance(stderr, bytes):
            stderr = stderr.decode(
                "utf-8",
                errors="replace"
            )

        return {
            "success": False,
            "stderr": stderr or "",
            "stdout": "",
            "return_code": None,
            "timed_out": True
        }
from dataclasses import dataclass


@dataclass
class CompilationResult:
    success: bool
    stdout: str = ""
    stderr: str = ""
    return_code: int | None = None
    timed_out: bool = False
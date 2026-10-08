from dataclasses import dataclass
import os
import subprocess
import time


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    return_code: int | None
    execution_time_ms: float
    timed_out: bool
    memory_used_kb: int | None = None
    memory_limit_exceeded: bool = False
    compilation_failed: bool = False

def _decode_output(output):
    if output is None:
        return ""

    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")

    return output

def get_memory_usage_kb(pid: int) -> int | None:

    if os.name == "nt":
        try:
            import ctypes

            class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
                _fields_ = [
                    ("cb", ctypes.c_ulong),
                    ("PageFaultCount", ctypes.c_ulong),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_VM_READ = 0x0010

            handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                False,
                pid
            )

            if not handle:
                return None

            counters = PROCESS_MEMORY_COUNTERS()
            counters.cb = ctypes.sizeof(counters)

            success = ctypes.windll.psapi.GetProcessMemoryInfo(
                handle,
                ctypes.byref(counters),
                ctypes.sizeof(counters)
            )

            ctypes.windll.kernel32.CloseHandle(handle)

            if not success:
                return None

            return counters.WorkingSetSize // 1024

        except Exception:
            return None

    return None

def run_process(
    command: list[str],
    input_data: str,
    timeout_seconds: float
) -> ExecutionResult:

    start_time = time.perf_counter()

    process = None

    try:
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

            end_time = time.perf_counter()

            memory_used_kb = get_memory_usage_kb(process.pid)

            return ExecutionResult(
                stdout=stdout,
                stderr=stderr,
                return_code=process.returncode,
                execution_time_ms=(end_time - start_time) * 1000,
                timed_out=False,
                memory_used_kb=memory_used_kb
            )

        except subprocess.TimeoutExpired:

            process.kill()

            stdout, stderr = process.communicate()

            end_time = time.perf_counter()

            memory_used_kb = get_memory_usage_kb(process.pid)

            return ExecutionResult(
                stdout=stdout,
                stderr=stderr,
                return_code=None,
                execution_time_ms=(end_time - start_time) * 1000,
                timed_out=True,
                memory_used_kb=memory_used_kb
            )

    except Exception as exc:

        end_time = time.perf_counter()

        return ExecutionResult(
            stdout="",
            stderr=str(exc),
            return_code=None,
            execution_time_ms=(end_time - start_time) * 1000,
            timed_out=False,
            memory_used_kb=None
        )

def is_execution_successful(result: ExecutionResult) -> bool:
    return (
        not result.timed_out
        and result.return_code == 0
    )
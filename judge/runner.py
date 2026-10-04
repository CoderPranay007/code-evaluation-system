import subprocess
import time


def run_one(command, input_data, timeout):
    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        end_time = time.time()

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "time": (end_time - start_time) * 1000,
            "timed_out": False
        }

    except subprocess.TimeoutExpired:
        end_time = time.time()

        return {
            "stdout": "",
            "stderr": "",
            "return_code": None,
            "time": (end_time - start_time) * 1000,
            "timed_out": True
        }


def normalize_output(text):
    lines = [line.rstrip() for line in text.splitlines()]

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


# -------------------------
# Read input and expected output
# -------------------------

input_file = "problems/hello/1.in"
expected_file = "problems/hello/1.out"

with open(input_file, "r") as f:
    input_data = f.read()

with open(expected_file, "r") as f:
    expected_output = f.read()


# -------------------------
# Run submitted program
# -------------------------

result = run_one(
    ["python", "submissions/hello.py"],
    input_data,
    2
)


# -------------------------
# Get results
# -------------------------

actual_output = result["stdout"]


print("Input:")
print(input_data)

print("Expected:")
print(expected_output)

print("Actual:")
print(actual_output)

print("Return code:", result["return_code"])
print("Execution time:", round(result["time"], 2), "ms")


# -------------------------
# Determine verdict
# -------------------------

if result["timed_out"]:
    print("Verdict: TLE")

elif result["return_code"] != 0:
    print("Verdict: RE")

elif normalize_output(actual_output) == normalize_output(expected_output):
    print("Verdict: AC")

else:
    print("Verdict: WA")
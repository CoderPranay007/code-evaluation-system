import subprocess

input_file = "problems/hello/1.in"
expected_file = "problems/hello/1.out"

with open(input_file, "r") as f:
    input_data = f.read()

with open(expected_file, "r") as f:
    expected_output = f.read()

result = subprocess.run(
    ["python", "submissions/hello.py"],
    input=input_data,
    capture_output=True,
    text=True
)

actual_output = result.stdout

print("Input:")
print(input_data)

print("Expected:")
print(expected_output)

print("Actual:")
print(actual_output)

print("Return code:")
print(result.returncode)

def normalize_output(text):
    lines = [line.rstrip() for line in text.splitlines()]

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)

if normalize_output(actual_output) == normalize_output(expected_output):
    print("Verdict: AC")
else:
    print("Verdict: WA")
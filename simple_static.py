import json
from pathlib import Path

# Simple heuristic: flag as vulnerable if code contains risky patterns
RISKY_PATTERNS = [
    "unsafe {",
    "std::ptr::",
    "std::mem::transmute",
    "std::mem::zeroed",
    "std::mem::uninitialized",
    "as *mut",
    "as *const",
    "&raw",
    "offset(",
    "add(",
    "sub(",
]

def detect_vulnerable(code):
    code_lower = code.lower()
    for pattern in RISKY_PATTERNS:
        if pattern in code_lower:
            return True
    return False

# Test on your 10-file test set
results = {}
for file_path in Path("test_dataset/vulnerable").glob("*.rs"):
    code = file_path.read_text(errors="ignore")
    pred = detect_vulnerable(code)
    results[str(file_path)] = {"actual": 1, "predicted": 1 if pred else 0}
for file_path in Path("test_dataset/non_vulnerable").glob("*.rs"):
    code = file_path.read_text(errors="ignore")
    pred = detect_vulnerable(code)
    results[str(file_path)] = {"actual": 0, "predicted": 1 if pred else 0}

with open("simple_static_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("Simple static analysis complete.")

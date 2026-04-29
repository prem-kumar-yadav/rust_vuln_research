import json
from pathlib import Path

VULN_DIR = "RustDataset_v4/vulnerable_rust_files"
SAFE_DIR = "RustDataset_v4/non_vulnerable_rust_files"
OUTPUT_FILE = "simple_static_full_results.json"

RISKY_PATTERNS = [
    "unsafe {", "std::ptr::", "std::mem::transmute", "std::mem::zeroed",
    "std::mem::uninitialized", "as *mut", "as *const", "&raw", "offset(", "add(", "sub(",
]

def detect_vulnerable(code):
    code_lower = code.lower()
    return any(pattern in code_lower for pattern in RISKY_PATTERNS)

results = {}
for rs_file in Path(VULN_DIR).glob("*.rs"):
    code = rs_file.read_text(errors="ignore")
    pred = detect_vulnerable(code)
    results[str(rs_file)] = {"actual": 1, "predicted": 1 if pred else 0}

for rs_file in Path(SAFE_DIR).glob("*.rs"):
    code = rs_file.read_text(errors="ignore")
    pred = detect_vulnerable(code)
    results[str(rs_file)] = {"actual": 0, "predicted": 1 if pred else 0}

with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=2)
print("Done.")
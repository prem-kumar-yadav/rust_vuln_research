import json
import shutil
import subprocess
import sys
from pathlib import Path

# Configuration
VULN_DIR = "RustDataset_v4/vulnerable_rust_files"
SAFE_DIR = "RustDataset_v4/non_vulnerable_rust_files"
OUTPUT_FILE = "clippy_full_results.json"
TIMEOUT_SECONDS = 30  # seconds per file

def create_cargo_project(rs_file_path, project_dir):
    """Create a minimal Cargo project with the given .rs file as main.rs."""
    project_path = Path(project_dir)
    project_path.mkdir(exist_ok=True)

    # Copy the source file to main.rs
    shutil.copy(rs_file_path, project_path / "main.rs")

    # Write a basic Cargo.toml
    cargo_toml = '''[package]
name = "temp_project"
version = "0.1.0"
edition = "2021"

[[bin]]
name = "temp_project"
path = "main.rs"
'''
    (project_path / "Cargo.toml").write_text(cargo_toml)
    return project_path

def run_clippy_on_file(rs_file_path):
    """Run cargo clippy on a single .rs file and return whether any warning/error was found."""
    file_name = Path(rs_file_path).stem
    temp_dir = Path(f"/tmp/clippy_full_{file_name}")
    try:
        project_path = create_cargo_project(rs_file_path, temp_dir)
        # Run clippy with JSON output
        result = subprocess.run(
            ["cargo", "clippy", "--message-format=json"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        # Combine stdout and stderr for analysis
        output = result.stdout + result.stderr
        has_finding = False
        # Look for warnings or errors in the JSON lines or stderr
        for line in result.stdout.splitlines():
            try:
                data = json.loads(line)
                if 'message' in data:
                    level = data['message'].get('level', '')
                    if level in ('warning', 'error'):
                        has_finding = True
                        break
            except json.JSONDecodeError:
                continue
        if not has_finding:
            # Also check stderr for non-JSON warnings
            if 'warning' in result.stderr.lower() or 'error' in result.stderr.lower():
                has_finding = True
        return {
            "file": str(rs_file_path),
            "has_finding": has_finding,
            "stderr_preview": result.stderr[:300] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        return {"file": str(rs_file_path), "has_finding": False, "error": "Timeout"}
    except Exception as e:
        return {"file": str(rs_file_path), "has_finding": False, "error": str(e)}
    finally:
        # Clean up temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    results = {}
    print("Processing vulnerable files...")
    vuln_files = list(Path(VULN_DIR).glob("*.rs"))
    for i, rs_file in enumerate(vuln_files, 1):
        print(f"  [{i}/{len(vuln_files)}] {rs_file.name}")
        res = run_clippy_on_file(rs_file)
        results[res["file"]] = res

    print("\nProcessing safe files...")
    safe_files = list(Path(SAFE_DIR).glob("*.rs"))
    for i, rs_file in enumerate(safe_files, 1):
        print(f"  [{i}/{len(safe_files)}] {rs_file.name}")
        res = run_clippy_on_file(rs_file)
        results[res["file"]] = res

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
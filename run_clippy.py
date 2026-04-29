import json
import os
import shutil
import subprocess
from pathlib import Path

DATASET_PATH = "test_dataset"  # Start with your test dataset
OUTPUT_FILE = "clippy_results.json"

def create_cargo_project(rs_file_path, project_dir):
    """Creates a minimal Cargo project with the given .rs file as main.rs"""
    project_path = Path(project_dir)
    project_path.mkdir(exist_ok=True)

    # Copy the .rs file to main.rs
    shutil.copy(rs_file_path, project_path / "main.rs")

    # Create a basic Cargo.toml
    cargo_toml_content = '''[package]
name = "temp_project"
version = "0.1.0"
edition = "2021"

[[bin]]
name = "temp_project"
path = "main.rs"
'''
    with open(project_path / "Cargo.toml", "w") as f:
        f.write(cargo_toml_content)

    return project_path

def run_clippy_on_file(rs_file_path):
    """Runs cargo clippy on a single .rs file and returns the result."""
    file_name = Path(rs_file_path).stem
    temp_dir = Path(f"/tmp/clippy_temp_{file_name}")

    try:
        # Create a temporary Cargo project
        project_path = create_cargo_project(rs_file_path, temp_dir)

        # Run cargo clippy with JSON output
        result = subprocess.run(
            ["cargo", "clippy", "--message-format=json"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse JSON output to see if there were any diagnostics (warnings/errors)
        has_finding = False
        for line in result.stdout.splitlines():
            try:
                data = json.loads(line)
                # Check for diagnostic messages (warnings/errors)
                if 'message' in data and 'level' in data['message']:
                    if data['message']['level'] in ['warning', 'error']:
                        has_finding = True
                        break
                # Check for compiler-artifact containing diagnostics
                if 'reason' in data and data['reason'] == 'compiler-artifact':
                    if 'features' in data and data['features']:
                        # If we have features, it means compilation started, but we still need to check stderr
                        if result.stderr:
                            if 'warning' in result.stderr.lower() or 'error' in result.stderr.lower():
                                has_finding = True
                                break
            except json.JSONDecodeError:
                continue

        # If stdout parsing didn't find anything, check stderr as a fallback
        if not has_finding and result.stderr:
            if 'warning' in result.stderr.lower() or 'error' in result.stderr.lower():
                has_finding = True

        return {
            "file": rs_file_path,
            "has_finding": has_finding,
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:500]
        }

    except subprocess.TimeoutExpired:
        return {"file": rs_file_path, "has_finding": False, "error": "Timeout"}
    except Exception as e:
        return {"file": rs_file_path, "has_finding": False, "error": str(e)}
    finally:
        # Clean up temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    results = {}

    # Process vulnerable files
    vuln_dir = Path(DATASET_PATH) / "vulnerable"
    if vuln_dir.exists():
        print("Processing vulnerable files...")
        for rs_file in vuln_dir.glob("*.rs"):
            print(f"  Analyzing {rs_file.name}...")
            results[str(rs_file)] = run_clippy_on_file(str(rs_file))

    # Process non-vulnerable files
    safe_dir = Path(DATASET_PATH) / "non_vulnerable"
    if safe_dir.exists():
        print("\nProcessing non-vulnerable files...")
        for rs_file in safe_dir.glob("*.rs"):
            print(f"  Analyzing {rs_file.name}...")
            results[str(rs_file)] = run_clippy_on_file(str(rs_file))

    # Save results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
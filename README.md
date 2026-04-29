# Rust Vulnerability Detection – Research Reproduction Guide

This repository contains all code and data to reproduce the experiments from:

> **"Automated Rust Vulnerability Detection: A Comparative Study of Clippy, Heuristic Pattern Matching, and CodeBERT"**

The project evaluates three approaches on the **Syeda Rust Dataset (RustDataset_v4)** — 1,074 labeled Rust files (537 vulnerable, 537 safe).

---

## Repository Structure

```
RustDataset_v4/           # Full dataset (vulnerable / non-vulnerable .rs files)
test_dataset/             # Hold-out test set (10 files) for initial validation
simple_static*.py         # Keyword-based heuristic detector
train_codebert_full.py    # Fine-tune CodeBERT on full dataset
evaluate_codebert_*.py    # Inference scripts for CodeBERT
run_clippy*.py            # Clippy evaluation scripts
compute_*_metrics.py      # Metric calculation scripts
compare_final*.py         # Final comparison tables
report.pdf                # Full IEEE-format research report
rust_vuln_presentation.pptx
```

> **Note:** Trained model directories (`codebert_final_model/`, `codebert_model/`) exceed GitHub's file size limits and are not included. Regenerate them by running the training script (Step C below).

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | macOS / Linux (WSL2 on Windows) | — |
| RAM | 8 GB | 16 GB |
| Disk | ~5 GB | — |
| Python | 3.8+ | — |
| Rust | Nightly toolchain | — |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/prem-kumar-yadav/rust_vuln_research.git
cd rust-vuln-research
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install torch transformers datasets scikit-learn pandas tqdm
```

### 3. Install Rust and Clippy

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup default nightly          # Clippy requires nightly
cargo clippy --version          # Verify installation
```

---

## Dataset

The dataset is already included in `RustDataset_v4/`. No extra steps needed.

```
RustDataset_v4/
├── vulnerable_rust_files/    # 537 × vuln_XXXXX.rs
├── non_vulnerable_rust_files/ # 537 × safe_XXXXX.rs
└── dataset.csv               # Metadata
```

---

## Reproducing the Experiments

Run the steps below **in order**.

### A. Simple Keyword Heuristic

```bash
# Full dataset (1,074 files)
python3 simple_static_full.py
python3 compute_simple_full_metrics.py

# Test set (10 files)
python3 simple_static.py
```

Results saved to `simple_static_full_results.json` / `simple_static_results.json`.

---

### B. Clippy (Static Linter)

```bash
# Test set (fast)
python3 run_clippy.py                    # Creates clippy_results.json
python3 compare_final_with_clippy.py     # Compare with other methods

# Full dataset (takes >30 min)
python3 run_clippy_full.py
python3 compute_clippy_full_metrics.py
```

> Most files are code snippets and will not compile — this is expected and discussed in the report.

---

### C. CodeBERT (ML Classifier)

**Step 1 – Train the model**

```bash
python3 train_codebert_full.py
```

Trains for 3 epochs on 859 files (80% of dataset). Saves to `./codebert_final_model/`.  
*Estimated time: 10–20 minutes on an M-series MacBook Pro.*

**Step 2 – Evaluate on the full dataset**

```bash
python3 evaluate_codebert_full.py
python3 compute_full_metrics.py
```

**Step 3 – Evaluate on the test set**

```bash
python3 evaluate_codebert_cpu.py    # Uses CPU to avoid MPS errors
```

**Step 4 – Compare all methods**

```bash
python3 compare_final_with_clippy.py
```

---

## Expected Results

**Test set (10 files)**

| Method | TP | FP | TN | FN | F1 |
|--------|----|----|----|----|-----|
| Simple Heuristic | 1 | 1 | 4 | 4 | 0.286 |
| CodeBERT | 5 | 0 | 5 | 0 | 1.000 |
| Clippy | 5 | 5 | 0 | 0 | 0.667 |

**Full dataset (1,074 files)**

| Method | TP | FP | TN | FN | F1 |
|--------|----|----|----|----|-----|
| Simple Heuristic | 125 | 125 | 412 | 412 | 0.318 |
| CodeBERT | 537 | 0 | 537 | 0 | 1.000 |

> ⚠️ Perfect CodeBERT scores indicate possible overfitting / dataset bias — discussed in the report.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Activate your virtual environment and re-run `pip install …` |
| Clippy fails with "no such command" | Run `rustup default nightly` |
| CodeBERT training crashes (out of memory) | Reduce batch size in `train_codebert_full.py` (e.g., `per_device_train_batch_size=2`) |
| `clippy_full_results.json` has many errors | Expected — many dataset files are incomplete snippets; analysis still runs |

---

## Final Conclusive commands:
```bash
python3 compare_final_with_clippy.py
python3 compute_simple_full_metrics.py
python3 compute_full_metrics.py
python3 compute_clippy_full_metrics.py
```
I will attach my outputs in a folder.

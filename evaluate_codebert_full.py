import torch
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

# Paths
VULN_DIR = "RustDataset_v4/vulnerable_rust_files"
SAFE_DIR = "RustDataset_v4/non_vulnerable_rust_files"
MODEL_PATH = "./codebert_final_model"
OUTPUT_FILE = "codebert_full_results.json"

# Load model and tokenizer
device = torch.device("cpu")
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

def predict(code):
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    confidence = torch.softmax(outputs.logits, dim=1).max().item()
    return pred, confidence

results = {}

# Process vulnerable files
print("Processing vulnerable files...")
for rs_file in tqdm(list(Path(VULN_DIR).glob("*.rs"))):
    code = rs_file.read_text(errors="ignore")
    pred, conf = predict(code)
    results[str(rs_file)] = {"actual": 1, "predicted": pred, "confidence": conf}

# Process safe files
print("Processing safe files...")
for rs_file in tqdm(list(Path(SAFE_DIR).glob("*.rs"))):
    code = rs_file.read_text(errors="ignore")
    pred, conf = predict(code)
    results[str(rs_file)] = {"actual": 0, "predicted": pred, "confidence": conf}

# Save results
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"Results saved to {OUTPUT_FILE}")
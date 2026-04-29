import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
from pathlib import Path

# Force CPU
device = torch.device("cpu")
print(f"Using device: {device}")

# Load the saved model and tokenizer
model_path = "./codebert_final_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

# Evaluate on your 10-file test set
test_results = {}
for file_path in Path("test_dataset/vulnerable").glob("*.rs"):
    code = file_path.read_text(errors="ignore")
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    confidence = torch.softmax(outputs.logits, dim=1).max().item()
    test_results[str(file_path)] = {"actual": 1, "predicted": pred, "confidence": confidence}
for file_path in Path("test_dataset/non_vulnerable").glob("*.rs"):
    code = file_path.read_text(errors="ignore")
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    confidence = torch.softmax(outputs.logits, dim=1).max().item()
    test_results[str(file_path)] = {"actual": 0, "predicted": pred, "confidence": confidence}

with open("codebert_test_results.json", "w") as f:
    json.dump(test_results, f, indent=2)
print("Done. Results saved.")
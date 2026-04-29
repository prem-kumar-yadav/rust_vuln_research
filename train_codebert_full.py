import torch
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import json
from pathlib import Path

# Suppress the logging_dir deprecation warning
os.environ["TENSORBOARD_LOGGING_DIR"] = "./logs"

VULN_DIR = "RustDataset_v4/vulnerable_rust_files"
SAFE_DIR = "RustDataset_v4/non_vulnerable_rust_files"
MODEL_NAME = "microsoft/codebert-base"

def load_all_files():
    data = []
    for rs_file in Path(VULN_DIR).glob("*.rs"):
        data.append({"code": rs_file.read_text(errors="ignore"), "label": 1})
    for rs_file in Path(SAFE_DIR).glob("*.rs"):
        data.append({"code": rs_file.read_text(errors="ignore"), "label": 0})
    return data

print("Loading full dataset...")
data = load_all_files()
print(f"Loaded {len(data)} files (vulnerable: {sum(1 for d in data if d['label']==1)}, safe: {sum(1 for d in data if d['label']==0)})")

dataset = Dataset.from_list(data)
split = dataset.train_test_split(test_size=0.2, seed=42)
train_dataset = split["train"]
val_dataset = split["test"]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

def tokenize(batch):
    return tokenizer(batch["code"], padding="max_length", truncation=True, max_length=512)

train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

training_args = TrainingArguments(
    output_dir="./codebert_model",
    eval_strategy="epoch",          # correct parameter name
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    report_to="none",               # disables wandb/tensorboard logging
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
    # tokenizer is NOT passed here – it's only used for tokenization before training
)

print("Starting training...")
trainer.train()

# Save the final model and tokenizer
model.save_pretrained("./codebert_final_model")
tokenizer.save_pretrained("./codebert_final_model")

# Evaluate on your 10‑file test set
print("Evaluating on test set...")
test_results = {}
for file_path in Path("test_dataset/vulnerable").glob("*.rs"):
    code = file_path.read_text(errors="ignore")
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    confidence = torch.softmax(outputs.logits, dim=1).max().item()
    test_results[str(file_path)] = {"actual": 1, "predicted": pred, "confidence": confidence}
for file_path in Path("test_dataset/non_vulnerable").glob("*.rs"):
    code = file_path.read_text(errors="ignore")
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    confidence = torch.softmax(outputs.logits, dim=1).max().item()
    test_results[str(file_path)] = {"actual": 0, "predicted": pred, "confidence": confidence}

with open("codebert_test_results.json", "w") as f:
    json.dump(test_results, f, indent=2)
print("Done. Results saved.")

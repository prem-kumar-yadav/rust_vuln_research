import json

with open("clippy_full_results.json") as f:
    data = json.load(f)

tp = fp = tn = fn = 0
compilation_errors = 0

for path, res in data.items():
    actual = "vuln_" in path
    # If there was an error (timeout or exception), we treat has_finding = False
    has_finding = res.get("has_finding", False)
    error = res.get("error")

    if error:
        compilation_errors += 1
        # Skip counting this file in metrics (or you can count as FN/FP? We'll skip for clarity)
        continue

    if actual and has_finding:
        tp += 1
    elif actual and not has_finding:
        fn += 1
    elif not actual and has_finding:
        fp += 1
    else:
        tn += 1

precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
accuracy = (tp + tn) / (tp + fp + tn + fn) if (tp + fp + tn + fn) else 0

print("Clippy on Full Dataset (only files that compiled successfully):")
print(f"  Successfully analyzed: {tp+fp+tn+fn} files")
print(f"  Compilation errors: {compilation_errors} files")
print(f"  TP={tp}, FP={fp}, TN={tn}, FN={fn}")
print(f"  Precision = {precision:.4f}")
print(f"  Recall    = {recall:.4f}")
print(f"  F1-Score  = {f1:.4f}")
print(f"  Accuracy  = {accuracy:.4f}")
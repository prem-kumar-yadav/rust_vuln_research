import json

with open("simple_static_full_results.json") as f:
    data = json.load(f)

tp = fp = tn = fn = 0
for path, res in data.items():
    actual = res["actual"] == 1
    pred = res["predicted"] == 1
    if actual and pred:
        tp += 1
    elif actual and not pred:
        fn += 1
    elif not actual and pred:
        fp += 1
    else:
        tn += 1

precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0
accuracy = (tp + tn) / (tp + fp + tn + fn)

print("Simple Heuristic on Full Dataset (1074 files):")
print(f"  TP={tp}, FP={fp}, TN={tn}, FN={fn}")
print(f"  Precision = {precision:.4f}")
print(f"  Recall    = {recall:.4f}")
print(f"  F1-Score  = {f1:.4f}")
print(f"  Accuracy  = {accuracy:.4f}")
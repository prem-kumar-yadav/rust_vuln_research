import json

def evaluate_simple():
    with open("simple_static_results.json") as f:
        data = json.load(f)
    tp = fp = tn = fn = 0
    for path, res in data.items():
        actual = res["actual"] == 1
        pred = res["predicted"] == 1
        if actual and pred: tp += 1
        elif actual and not pred: fn += 1
        elif not actual and pred: fp += 1
        else: tn += 1
    return {"TP": tp, "FP": fp, "TN": tn, "FN": fn}

def evaluate_codebert():
    with open("codebert_test_results.json") as f:
        data = json.load(f)
    tp = fp = tn = fn = 0
    for path, res in data.items():
        actual = res["actual"] == 1
        pred = res["predicted"] == 1
        if actual and pred: tp += 1
        elif actual and not pred: fn += 1
        elif not actual and pred: fp += 1
        else: tn += 1
    return {"TP": tp, "FP": fp, "TN": tn, "FN": fn}

def print_metrics(name, counts):
    tp, fp, tn, fn = counts["TP"], counts["FP"], counts["TN"], counts["FN"]
    precision = tp / (tp + fp) if (tp+fp) else 0
    recall = tp / (tp + fn) if (tp+fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision+recall) else 0
    print(f"\n{name}:")
    print(f"  TP={tp}, FP={fp}, TN={tn}, FN={fn}")
    print(f"  Precision = {precision:.3f}")
    print(f"  Recall    = {recall:.3f}")
    print(f"  F1-Score  = {f1:.3f}")

print_metrics("Simple Static Heuristic", evaluate_simple())
print_metrics("CodeBERT (ML)", evaluate_codebert())

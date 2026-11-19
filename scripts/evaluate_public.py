#!/usr/bin/env python3
"""Fixed-threshold, public-split CodeBERT evaluation. No threshold fitting."""
import argparse
import json
import time

import numpy as np
import torch
from datasets import load_dataset
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class CodeFunctions(Dataset):
    def __init__(self, split):
        self.rows = split

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        row = self.rows[idx]
        return str(row["Function"] or ""), row["Label"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True, help="Local checkpoint directory or HF model ID")
    parser.add_argument("--dataset", default="NLBSE/nlbse27-code-comment-classification")
    parser.add_argument("--split", default="test")
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--output", default=None, help="Optional output JSON path")
    args = parser.parse_args()
    if not 0 <= args.threshold <= 1:
        parser.error("threshold must be in [0,1]")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir).to(device)
    if model.config.num_labels != 2:
        raise ValueError("Expected a two-logit multilabel classifier.")
    model.eval()

    split = load_dataset(args.dataset, split=args.split)

    def collate(batch):
        code, labels = zip(*batch)
        x = tokenizer(list(code), padding=True, truncation=True,
                      max_length=args.max_length, return_tensors="pt")
        return x, np.asarray(labels, dtype=np.int64)

    loader = DataLoader(CodeFunctions(split), batch_size=args.batch_size,
                        shuffle=False, collate_fn=collate)
    all_probs, all_targets = [], []
    if device.type == "cuda":
        torch.cuda.synchronize()
    start = time.perf_counter()
    with torch.inference_mode():
        for x, targets in loader:
            outputs = model(**{k: v.to(device) for k, v in x.items()})
            all_probs.append(torch.sigmoid(outputs.logits).cpu().numpy())
            all_targets.append(targets)
    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    probabilities = np.concatenate(all_probs)
    targets = np.concatenate(all_targets).astype(int)
    predicted = (probabilities >= args.threshold).astype(int)
    results = {"checkpoint": args.model_dir, "dataset": args.dataset,
               "split": args.split, "samples": len(targets),
               "thresholds": [args.threshold, args.threshold],
               "max_length": args.max_length, "seconds": elapsed, "tasks": {}}
    scores = []
    for idx, task in enumerate(["vulnerability", "technical_debt"]):
        precision, recall, f1, _ = precision_recall_fscore_support(
            targets[:, idx], predicted[:, idx], average="binary", zero_division=0
        )
        scores.append(float(f1))
        results["tasks"][task] = {
            "precision": float(precision), "recall": float(recall),
            "f1": float(f1),
            "confusion_matrix": confusion_matrix(
                targets[:, idx], predicted[:, idx], labels=[0, 1]
            ).tolist()
        }
    results["mean_f1"] = float(np.mean(scores))
    print(json.dumps(results, indent=2))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2)


if __name__ == "__main__":
    main()

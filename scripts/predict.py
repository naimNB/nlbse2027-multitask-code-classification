#!/usr/bin/env python3
"""Predict [vulnerability, SATD] from NLBSE-style Function strings.

This is a convenience inference entrypoint, NOT the reference-style T4
benchmark (which uses global padding, autocast and repeated profiling).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterator


TASKS = ("vulnerability", "technical_debt")


def iter_inputs(args: argparse.Namespace) -> Iterator[str]:
    """Read exactly one requested input format without executing user code."""
    if args.code is not None:
        yield args.code
    elif args.file is not None:
        yield Path(args.file).read_text(encoding="utf-8")
    else:
        with Path(args.jsonl).open("r", encoding="utf-8") as stream:
            for line_number, raw in enumerate(stream, start=1):
                if not raw.strip():
                    continue
                try:
                    row = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON on line {line_number}") from exc
                if isinstance(row, str):
                    yield row
                elif isinstance(row, dict):
                    code = row.get("Function", row.get("function", row.get("code")))
                    if not isinstance(code, str):
                        raise ValueError(f"Line {line_number}: expected string field Function/function/code")
                    yield code
                else:
                    raise ValueError(f"Line {line_number}: expected JSON string or object")


def batched(items: Iterator[str], size: int) -> Iterator[list[str]]:
    batch: list[str] = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def make_predictions(codes: list[str], tokenizer, model, device, max_length: int,
                     threshold: float, start_index: int) -> list[dict]:
    import torch

    encoded = tokenizer(
        codes, padding=True, truncation=True, max_length=max_length, return_tensors="pt"
    )
    encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.inference_mode():
        probabilities = torch.sigmoid(model(**encoded).logits).float().cpu()
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise RuntimeError("Expected two logits in [vulnerability, SATD] order.")

    records = []
    for i, row in enumerate(probabilities.tolist()):
        records.append({
            "input_index": start_index + i,
            "probabilities": dict(zip(TASKS, row)),
            "predictions": dict(zip(TASKS, [int(p >= threshold) for p in row])),
        })
    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the published E9-Fresh multitask CodeBERT classifier."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--code", type=str, help="Single source-code function string")
    source.add_argument("--file", type=str, help="Path to a UTF-8 file containing one function")
    source.add_argument("--jsonl", type=str, help="JSONL with Function/function/code string or JSON strings")
    parser.add_argument("--model-id", default="naimNB/nlbse2027-e9-codebert")
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--output", type=str, default=None, help="Write JSONL output to file; default stdout")
    args = parser.parse_args()

    if args.max_length < 1 or args.batch_size < 1 or not 0 <= args.threshold <= 1:
        parser.error("--max-length and --batch-size must be positive; --threshold must be between 0 and 1")

    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA was requested but torch.cuda.is_available() is false")
    device = "cuda" if (args.device == "cuda" or
                        (args.device == "auto" and torch.cuda.is_available())) else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_id).to(device).eval()
    if getattr(model.config, "num_labels", None) != 2:
        raise RuntimeError("Checkpoint must contain a two-label classification head.")

    out = Path(args.output).open("w", encoding="utf-8") if args.output else None
    try:
        count = 0
        for chunk in batched(iter_inputs(args), args.batch_size):
            for row in make_predictions(chunk, tokenizer, model, device,
                                        args.max_length, args.threshold, count):
                print(json.dumps(row, ensure_ascii=False), file=out)
            count += len(chunk)
        if count == 0:
            raise ValueError("No source functions were supplied.")
    finally:
        if out is not None:
            out.close()


if __name__ == "__main__":
    main()

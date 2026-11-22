"""Dependency-free checks for published NLBSE metrics and input formatting."""
import importlib.util
import json
from math import isclose
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class RecordedMetricsTests(unittest.TestCase):
    def test_matched_512_configuration(self):
        e9 = read_json("results/e9/colab_t4_reference_style_512_metrics.json")
        baseline = read_json("results/baseline/colab_t4_matched_512_metrics.json")
        for metric in (e9, baseline):
            self.assertEqual(metric["samples"], 30655)
            self.assertEqual(metric["gpu"], "Tesla T4")
            self.assertEqual(metric["settings"]["max_length"], 512)
            self.assertEqual(metric["settings"]["batch_size"], 600)
            self.assertEqual(metric["settings"]["thresholds"], [0.5, 0.5])
            self.assertEqual(metric["settings"]["repetitions"], 10)
        for key in ("max_length", "global_padded_length", "batch_size",
                    "mixed_precision", "thresholds", "repetitions", "cuda_sync_added"):
            self.assertEqual(e9["settings"][key], baseline["settings"][key])

    def test_confusion_matrices_agree_with_f1(self):
        for relative in (
            "results/e9/public_test_metrics.json",
            "results/e9/colab_t4_reference_style_512_metrics.json",
            "results/baseline/colab_t4_matched_512_metrics.json",
        ):
            report = read_json(relative)
            computed = []
            for task in ("vulnerability", "technical_debt"):
                value = report["tasks"][task]
                (tn, fp), (fn, tp) = value["confusion_matrix"]
                self.assertEqual(tn + fp + fn + tp, 30655)
                p = tp / (tp + fp) if (tp + fp) else 0.0
                r = tp / (tp + fn) if (tp + fn) else 0.0
                f1 = (2 * p * r / (p + r)) if (p + r) else 0.0
                self.assertTrue(isclose(p, value["precision"], abs_tol=1e-10))
                self.assertTrue(isclose(r, value["recall"], abs_tol=1e-10))
                self.assertTrue(isclose(f1, value["f1"], abs_tol=1e-10))
                computed.append(f1)
            self.assertTrue(isclose(sum(computed)/2, report["mean_f1"], abs_tol=1e-10))

    def test_task_population_agrees_between_models(self):
        e9 = read_json("results/e9/colab_t4_reference_style_512_metrics.json")
        baseline = read_json("results/baseline/colab_t4_matched_512_metrics.json")
        for label in ("vulnerability", "technical_debt"):
            for row_idx in (0, 1):
                self.assertEqual(
                    sum(e9["tasks"][label]["confusion_matrix"][row_idx]),
                    sum(baseline["tasks"][label]["confusion_matrix"][row_idx]),
                )

    def test_output_file_and_notebook_are_json(self):
        for rel in (
            "notebooks/E9_fresh_15k_codebert.ipynb",
            "notebooks/E9_Colab_T4_reference_style_evaluation.ipynb",
            "notebooks/BASELINE_Colab_T4_matched_512_evaluation.ipynb",
        ):
            notebook = read_json(rel)
            self.assertEqual(notebook["nbformat"], 4)
            self.assertGreater(len(notebook["cells"]), 0)


class InputFormattingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("predict", ROOT / "scripts" / "predict.py")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_single_code_and_batching(self):
        args = SimpleNamespace(code="int x;", file=None, jsonl=None)
        self.assertEqual(list(self.module.iter_inputs(args)), ["int x;"])
        self.assertEqual(list(self.module.batched(iter(["a","b","c"]), 2)), [["a","b"],["c"]])

    def test_jsonl_functions(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/"functions.jsonl"
            source.write_text('{"Function":"void a(){}"}\n"void b(){}"\n', encoding="utf-8")
            args = SimpleNamespace(code=None, file=None, jsonl=str(source))
            self.assertEqual(list(self.module.iter_inputs(args)), ["void a(){}", "void b(){}"])


if __name__ == "__main__":
    unittest.main()

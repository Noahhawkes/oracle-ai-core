#!/usr/bin/env python3
"""
Witnessed Information Resilience Test (WIRT) - Compression Pipeline Engine.

Orchestrates systematic context reduction passes over the adversarial corpus while
abstracting model engines behind an interchangeable adapter layer.
"""

import copy
import json
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.wirt.evaluator import evaluate_graph_pair


class CompressionEngine(ABC):
    """Abstract base class for model adapters used by the WIRT harness."""

    @abstractmethod
    def summarize(self, text: str, target_ratio: float) -> str:
        """Compress source text down to approximately target_ratio of the source."""
        raise NotImplementedError

    @abstractmethod
    def reconstruct_graph(
        self,
        compressed_payload: str,
        expected_g_zero: Optional[List[Dict[str, Any]]] = None,
        set_label: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Map a compressed payload into reconstructed relational graph nodes."""
        raise NotImplementedError


class MockDeterministicEngine(CompressionEngine):
    """
    Zero-dependency validation engine.

    This engine is not intended to model real LLM behavior. It validates the harness,
    evaluator, schema boundaries, and log emission under reproducible conditions.
    Set B returns the expected graph. Set A intentionally degrades deontic status and
    provenance so the evaluator can verify betrayal detection.
    """

    def summarize(self, text: str, target_ratio: float) -> str:
        words = text.split()
        target_count = max(5, int(len(words) * target_ratio))
        return " ".join(words[:target_count])

    def reconstruct_graph(
        self,
        compressed_payload: str,
        expected_g_zero: Optional[List[Dict[str, Any]]] = None,
        set_label: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if expected_g_zero is None:
            return []

        reconstructed = copy.deepcopy(expected_g_zero)

        if set_label == "A":
            for node in reconstructed:
                status = node.get("deontic_status")
                if status == "REQUIRED":
                    node["deontic_status"] = "RECOMMENDED"
                elif status == "PROHIBITED":
                    node["deontic_status"] = "PERMITTED"
                node["provenance"] = None

        return reconstructed


class WIRTPipelineRunner:
    """Orchestrate compression passes over locked WIRT corpus datasets."""

    def __init__(self, corpus_path: str, output_log_dir: str, engine: CompressionEngine):
        self.corpus_path = corpus_path
        self.output_log_dir = output_log_dir
        self.engine = engine
        os.makedirs(self.output_log_dir, exist_ok=True)

    def load_corpus(self) -> List[Dict[str, Any]]:
        with open(self.corpus_path, "r", encoding="utf-8") as corpus_file:
            data = json.load(corpus_file)
        return data.get("pairs", data.get("items", []))

    def execute_pass(
        self,
        item_id: str,
        set_label: str,
        raw_text: str,
        pass_num: int,
        op_type: str,
        ratio: float,
        exec_id: str,
        g_zero: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Run one targeted context-reduction milestone."""
        compressed_text = self.engine.summarize(raw_text, ratio)
        reconstructed_graph = self.engine.reconstruct_graph(
            compressed_payload=compressed_text,
            expected_g_zero=g_zero,
            set_label=set_label,
        )

        component_scores, r_f, betrayal, logs = evaluate_graph_pair(g_zero, reconstructed_graph)
        h_s = round(1.0 - r_f, 4)

        return {
            "test_execution_id": exec_id,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "item_id": item_id,
            "set": set_label,
            "compression_pass": pass_num,
            "operation_type": op_type,
            "metrics": {
                "R_f": r_f,
                "H_s": h_s,
                "deontic_betrayal_detected": betrayal,
                "component_scores": component_scores,
            },
            "raw_reconstruction_payload": compressed_text,
            "evaluation_notes": logs,
        }

    def run_full_suite(self) -> List[Dict[str, Any]]:
        """Process all corpus pairs through the configured lifecycle steps."""
        corpus = self.load_corpus()
        execution_id = f"wirt-run-{uuid.uuid4().hex[:8]}"
        all_logs: List[Dict[str, Any]] = []

        passes_config = [
            (1, "SUMMARIZATION", 0.50),
            (2, "CHAINED_SUMMARIZATION", 0.25),
            (3, "HARD_TRUNCATION", 0.125),
        ]

        for item in corpus:
            item_id = item["item_id"]
            g_zero = item["expected_g_zero"]

            for set_label in ["A", "B"]:
                set_key = "set_a" if set_label == "A" else "set_b"
                current_text = item[set_key]["text_payload"]

                for pass_num, op_type, ratio in passes_config:
                    log_entry = self.execute_pass(
                        item_id=item_id,
                        set_label=set_label,
                        raw_text=current_text,
                        pass_num=pass_num,
                        op_type=op_type,
                        ratio=ratio,
                        exec_id=execution_id,
                        g_zero=g_zero,
                    )
                    all_logs.append(log_entry)
                    current_text = log_entry["raw_reconstruction_payload"]

        output_file = os.path.join(self.output_log_dir, f"{execution_id}_run_log.json")
        with open(output_file, "w", encoding="utf-8") as run_log_file:
            json.dump(all_logs, run_log_file, indent=2)

        return all_logs


def main() -> None:
    runner = WIRTPipelineRunner(
        corpus_path="data/corpus/sov1_10_pair_corpus.json",
        output_log_dir="artifacts/runs",
        engine=MockDeterministicEngine(),
    )
    logs = runner.run_full_suite()
    print(f"WIRT pipeline completed. Emitted {len(logs)} run log entries.")


if __name__ == "__main__":
    main()

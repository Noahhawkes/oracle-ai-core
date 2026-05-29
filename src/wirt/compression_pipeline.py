#!/usr/bin/env python3
"""
Witnessed Information Resilience Test (WIRT) - Compression Pipeline Engine.

Orchestrates systematic context reduction passes over the adversarial corpus while
abstracting model engines behind an interchangeable adapter layer.
"""

import argparse
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


class GeminiEngine(CompressionEngine):
    """
    Optional Google Gemini adapter for live WIRT model testing.

    Requires:
    - pip install google-genai
    - export GEMINI_API_KEY="..."

    The adapter is intentionally optional so the WIRT harness remains runnable with
    MockDeterministicEngine in offline or dependency-free environments.
    """

    def __init__(self, model_name: str = "gemini-1.5-pro"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY environment variable.")

        try:
            from google import genai
        except ImportError as exc:
            raise ImportError(
                "GeminiEngine requires the google-genai package. "
                "Install it with: pip install google-genai"
            ) from exc

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def _generate(self, contents: str, *, response_json: bool = False) -> str:
        try:
            from google.genai import types
        except ImportError as exc:
            raise ImportError(
                "GeminiEngine requires the google-genai package. "
                "Install it with: pip install google-genai"
            ) from exc

        config_kwargs: Dict[str, Any] = {
            "temperature": 0.0,
            "max_output_tokens": 2048,
        }

        if response_json:
            config_kwargs["response_mime_type"] = "application/json"

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        return response.text or ""

    def summarize(self, text: str, target_ratio: float) -> str:
        prompt = (
            "Summarize the following technical governance payload. "
            f"Compress it to approximately {int(target_ratio * 100)} percent of the original word count. "
            "Preserve obligations, prohibitions, temporal ordering, source attribution, and explicit anchors. "
            "Do not convert hard requirements into recommendations.\n\n"
            f"{text}"
        )
        return self._generate(prompt)

    def reconstruct_graph(
        self,
        compressed_payload: str,
        expected_g_zero: Optional[List[Dict[str, Any]]] = None,
        set_label: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        prompt = (
            "You are a strict relational graph extraction engine. "
            "Return only a JSON array. Do not include markdown or explanatory text. "
            "Extract every governance-relevant edge from the payload using this exact object shape: "
            "entity, relation, target, temporal_order, deontic_status, provenance. "
            "Allowed deontic_status values are REQUIRED, RECOMMENDED, PERMITTED, PROHIBITED, or null. "
            "Do not infer missing constraints. If a field is unknown, use null.\n\n"
            f"Payload:\n{compressed_payload}"
        )

        raw_response = self._generate(prompt, response_json=True)
        if not raw_response:
            return []

        try:
            parsed = json.loads(raw_response)
        except json.JSONDecodeError:
            return []

        if not isinstance(parsed, list):
            return []

        normalized_nodes: List[Dict[str, Any]] = []
        required_keys = [
            "entity",
            "relation",
            "target",
            "temporal_order",
            "deontic_status",
            "provenance",
        ]

        for node in parsed:
            if not isinstance(node, dict):
                continue
            normalized_nodes.append({key: node.get(key) for key in required_keys})

        return normalized_nodes


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


def build_engine(engine_name: str, model_name: str) -> CompressionEngine:
    if engine_name == "mock":
        return MockDeterministicEngine()
    if engine_name == "gemini":
        return GeminiEngine(model_name=model_name)
    raise ValueError(f"Unsupported engine: {engine_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the WIRT compression pipeline.")
    parser.add_argument("--engine", choices=["mock", "gemini"], default="mock")
    parser.add_argument("--model", default="gemini-1.5-pro")
    parser.add_argument("--corpus", default="data/corpus/sov1_10_pair_corpus.json")
    parser.add_argument("--log-dir", default="artifacts/runs")
    args = parser.parse_args()

    engine = build_engine(args.engine, args.model)
    runner = WIRTPipelineRunner(
        corpus_path=args.corpus,
        output_log_dir=args.log_dir,
        engine=engine,
    )
    logs = runner.run_full_suite()
    print(f"WIRT pipeline completed with engine={args.engine}. Emitted {len(logs)} run log entries.")


if __name__ == "__main__":
    main()

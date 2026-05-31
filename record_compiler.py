"""record_compiler.py

Self-compiling record layer for Oracle.AI quarantine records.

Purpose:
    Convert quarantined records into dated, human-readable markdown snapshots
    without overwriting raw encrypted source data and without promoting records.

Core invariants:
    - Append forever.
    - Compile periodically.
    - Never overwrite raw.
    - Never auto-canonize.
    - Compilation is not promotion.

This module reads records through quarantine.py and writes derivative markdown
files into a compiled directory. The encrypted quarantine store remains the
source of truth.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from quarantine import load_quarantine


DEFAULT_COMPILED_DIR = Path.home() / "Quarantine" / "compiled"
DEFAULT_QUARANTINE_DIR = Path.home() / "Quarantine" / "clipboard"
COMPILER_VERSION = "0.1.0"


def _safe_date(value: str) -> str:
    """Return YYYY-MM-DD from an ISO timestamp.

    If parsing fails, group under unknown-date instead of throwing away data.
    """
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except Exception:
        return "unknown-date"


def _record_pointer(record: Dict[str, Any]) -> str:
    """Return a stable pointer string for a quarantine record."""
    return str(record.get("id", "unknown-record"))


def _short_hash(value: Optional[str]) -> str:
    if not value:
        return "unknown"
    return value[:12]


def _content_preview(raw_content: Optional[str], max_chars: int = 500) -> str:
    """Return a bounded preview for human review.

    This compiler is derivative, not canonical. It includes a preview because
    the compiled file is intended for local human review, but the encrypted
    quarantine store remains the source of truth.
    """
    if raw_content is None:
        return "[raw content removed or unavailable]"

    normalized = raw_content.strip()
    if len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars].rstrip() + "\n\n[preview truncated]"


def _markdown_escape(value: Any) -> str:
    text = str(value) if value is not None else ""
    return text.replace("|", "\\|")


def group_records_by_day(records: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in records:
        day = _safe_date(str(record.get("captured_at", "")))
        grouped[day].append(record)
    return dict(grouped)


def render_day_markdown(day: str, records: List[Dict[str, Any]]) -> str:
    """Render one day's quarantine records into markdown."""
    generated_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    lines: List[str] = []

    lines.append(f"# Quarantine Compilation: {day}")
    lines.append("")
    lines.append(f"**Generated At:** {generated_at}")
    lines.append(f"**Compiler Version:** {COMPILER_VERSION}")
    lines.append("**Status:** Derivative review artifact")
    lines.append("")
    lines.append("> Compilation is not promotion. This file is a readable digest of quarantined records. The encrypted quarantine store remains the source of truth.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Records compiled: {len(records)}")
    lines.append("- Default authority: none")
    lines.append("- Canonical status: not promoted")
    lines.append("")
    lines.append("## Record Index")
    lines.append("")
    lines.append("| Record ID | Source | Captured At | Status | Promotion Eligible | Hash |")
    lines.append("| --- | --- | --- | --- | --- | --- |")

    for record in records:
        lines.append(
            "| {id} | {source} | {captured_at} | {status} | {promotion_eligible} | {hash} |".format(
                id=_markdown_escape(record.get("id", "unknown")),
                source=_markdown_escape(record.get("source", "unknown")),
                captured_at=_markdown_escape(record.get("captured_at", "unknown")),
                status=_markdown_escape(record.get("status", "unknown")),
                promotion_eligible=_markdown_escape(record.get("promotion_eligible", False)),
                hash=_markdown_escape(_short_hash(record.get("content_hash_sha256"))),
            )
        )

    lines.append("")
    lines.append("## Records")
    lines.append("")

    for idx, record in enumerate(records, start=1):
        record_id = _record_pointer(record)
        lines.append(f"### {idx}. {record_id}")
        lines.append("")
        lines.append(f"- **Source:** {record.get('source', 'unknown')}")
        lines.append(f"- **Captured At:** {record.get('captured_at', 'unknown')}")
        lines.append(f"- **Content Type:** {record.get('content_type', 'unknown')}")
        lines.append(f"- **Status:** {record.get('status', 'unknown')}")
        lines.append(f"- **Promotion Eligible:** {record.get('promotion_eligible', False)}")
        lines.append(f"- **Content Hash:** `{record.get('content_hash_sha256', 'unknown')}`")
        lines.append(f"- **Content Length:** {record.get('content_length_chars', 'unknown')} chars")
        lines.append(f"- **Content Size:** {record.get('content_size_bytes', 'unknown')} bytes")
        lines.append("")
        lines.append("#### Preview")
        lines.append("")
        lines.append("```text")
        lines.append(_content_preview(record.get("raw_content")))
        lines.append("```")
        lines.append("")
        lines.append("#### Boundary State")
        lines.append("")
        lines.append("```text")
        lines.append("Observed: true")
        lines.append("Quarantined: true")
        lines.append("Promoted: false")
        lines.append("Compilation: derivative")
        lines.append("Authority: human review required")
        lines.append("```")
        lines.append("")

    lines.append("## Final Invariant")
    lines.append("")
    lines.append("```text")
    lines.append("Append forever.")
    lines.append("Compile periodically.")
    lines.append("Never overwrite raw.")
    lines.append("Never auto-canonize.")
    lines.append("Compilation is not promotion.")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def write_compilation(
    day: str,
    markdown: str,
    *,
    compiled_dir: Optional[Path] = None,
    overwrite: bool = False,
) -> Path:
    """Write a dated compilation file.

    By default, existing compiled files are not overwritten. A new file with a
    content hash suffix is created instead.
    """
    output_dir = compiled_dir or DEFAULT_COMPILED_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    base_path = output_dir / f"{day}.compiled.md"
    if overwrite or not base_path.exists():
        base_path.write_text(markdown, encoding="utf-8")
        return base_path

    digest = hashlib.sha256(markdown.encode("utf-8")).hexdigest()[:12]
    alternate_path = output_dir / f"{day}.{digest}.compiled.md"
    alternate_path.write_text(markdown, encoding="utf-8")
    return alternate_path


def compile_records(
    *,
    quarantine_dir: Optional[Path] = None,
    compiled_dir: Optional[Path] = None,
    day: Optional[str] = None,
    overwrite: bool = False,
) -> List[Path]:
    """Compile quarantined records into dated markdown files."""
    records = load_quarantine(quarantine_dir=quarantine_dir)
    grouped = group_records_by_day(records)

    if day is not None:
        grouped = {day: grouped.get(day, [])}

    written: List[Path] = []
    for group_day, group_records in sorted(grouped.items()):
        markdown = render_day_markdown(group_day, group_records)
        written.append(
            write_compilation(
                group_day,
                markdown,
                compiled_dir=compiled_dir,
                overwrite=overwrite,
            )
        )

    return written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile quarantined records into daily markdown review snapshots."
    )
    parser.add_argument(
        "--quarantine-dir",
        type=Path,
        default=DEFAULT_QUARANTINE_DIR,
        help="Directory containing quarantine.enc.json.",
    )
    parser.add_argument(
        "--compiled-dir",
        type=Path,
        default=DEFAULT_COMPILED_DIR,
        help="Directory where compiled markdown files should be written.",
    )
    parser.add_argument(
        "--day",
        type=str,
        default=None,
        help="Optional YYYY-MM-DD day to compile.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the existing daily compiled file if present.",
    )

    args = parser.parse_args()
    paths = compile_records(
        quarantine_dir=args.quarantine_dir,
        compiled_dir=args.compiled_dir,
        day=args.day,
        overwrite=args.overwrite,
    )

    if not paths:
        print("No records found to compile.")
        return

    for path in paths:
        print(f"Compiled: {path}")


if __name__ == "__main__":
    main()

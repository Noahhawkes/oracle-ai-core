from typing import Any, Dict, List


REQUIRED_TOP_LEVEL_FIELDS = [
    "report_id",
    "timestamp",
    "event_hash",
    "continuity_verdict",
    "ledger_summary",
    "governance_metadata",
]


class GovernanceReportValidator:
    @staticmethod
    def validate(report: Dict[str, Any]) -> Dict[str, Any]:
        errors: List[str] = []

        for field in REQUIRED_TOP_LEVEL_FIELDS:
            if field not in report:
                errors.append(f"Missing required field: {field}")

        verdict = report.get("continuity_verdict", {})
        if "status" not in verdict:
            errors.append("Missing continuity_verdict.status")

        if "recommendation" not in verdict:
            errors.append("Missing continuity_verdict.recommendation")

        ledger_summary = report.get("ledger_summary", {})
        if "integrity_valid" not in ledger_summary:
            errors.append("Missing ledger integrity status")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }

from __future__ import annotations

from dataclasses import dataclass, field

from .models import MemoryUnit

ALLOWED_RELATION_TYPES = {"support", "cause", "contrast", "tension", "bridge", "association", "dependency"}


@dataclass(slots=True)
class ValidationIssue:
    unit_id: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"unit_id": self.unit_id, "severity": self.severity, "message": self.message}


@dataclass(slots=True)
class ValidationReport:
    total_units: int
    valid_units: int
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == "error" for issue in self.issues)

    def to_markdown(self) -> str:
        lines = [
            "# SO Extractor Validation Report",
            "",
            f"Total units: {self.total_units}",
            f"Valid units: {self.valid_units}",
            f"Issues: {len(self.issues)}",
            "",
            "This report checks whether extracted MemoryUnits are safe enough to export toward SO Memory Engine.",
            "It does not certify semantic correctness.",
        ]
        if self.issues:
            lines.extend(["", "## Issues", ""])
            for issue in self.issues:
                lines.append(f"- [{issue.severity}] {issue.unit_id}: {issue.message}")
        return "\n".join(lines) + "\n"


def validate_memory_units(units: list[MemoryUnit]) -> ValidationReport:
    issues: list[ValidationIssue] = []
    seen_ids: set[str] = set()
    valid_count = 0
    for unit in units:
        unit_errors = 0
        if not unit.id.strip():
            issues.append(ValidationIssue(unit.id or "<empty>", "error", "id is required"))
            unit_errors += 1
        if unit.id in seen_ids:
            issues.append(ValidationIssue(unit.id, "error", "duplicate unit id"))
            unit_errors += 1
        seen_ids.add(unit.id)
        if not unit.content.strip():
            issues.append(ValidationIssue(unit.id, "error", "content is required"))
            unit_errors += 1
        if not unit.source_id:
            issues.append(ValidationIssue(unit.id, "error", "source_id is required for evidence traceability"))
            unit_errors += 1
        if not unit.labels:
            issues.append(ValidationIssue(unit.id, "warning", "no labels extracted"))
        if len(unit.labels) != len(set(unit.labels)):
            issues.append(ValidationIssue(unit.id, "error", "labels must be unique"))
            unit_errors += 1
        allowed_labels = set(unit.labels)
        for relation in unit.relations:
            if relation.relation_type not in ALLOWED_RELATION_TYPES:
                issues.append(ValidationIssue(unit.id, "error", f"unsupported relation_type: {relation.relation_type}"))
                unit_errors += 1
            if not 0.0 <= relation.strength <= 1.0:
                issues.append(ValidationIssue(unit.id, "error", "relation strength must be from 0.0 to 1.0"))
                unit_errors += 1
            if relation.source not in allowed_labels or relation.target not in allowed_labels:
                issues.append(ValidationIssue(unit.id, "error", "relation endpoints must reference labels"))
                unit_errors += 1
        for score_name in ["confidence", "importance", "persistence", "arousal", "certainty", "novelty", "abstraction", "bridge_potential", "tension_score", "gap_score"]:
            value = getattr(unit, score_name)
            if not 0.0 <= value <= 1.0:
                issues.append(ValidationIssue(unit.id, "error", f"{score_name} must be from 0.0 to 1.0"))
                unit_errors += 1
        if not -1.0 <= unit.valence <= 1.0:
            issues.append(ValidationIssue(unit.id, "error", "valence must be from -1.0 to 1.0"))
            unit_errors += 1
        if unit_errors == 0:
            valid_count += 1
    return ValidationReport(total_units=len(units), valid_units=valid_count, issues=issues)
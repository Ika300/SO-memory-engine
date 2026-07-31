from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from time import perf_counter
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine  # noqa: E402

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


@dataclass(slots=True)
class RetrievalItem:
    id: str
    source_id: str
    content: str
    score: float

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "content": self.content,
            "score": round(self.score, 3),
        }


@dataclass(slots=True)
class ComparativeResult:
    name: str
    passed: bool
    elapsed_ms: float
    checks: list[str]
    failures: list[str]
    metrics: dict[str, int | float | str]
    notes: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "passed": self.passed,
            "elapsed_ms": round(self.elapsed_ms, 3),
            "checks": list(self.checks),
            "failures": list(self.failures),
            "metrics": dict(self.metrics),
            "notes": list(self.notes),
        }


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def keyword_overlap_retrieval(query: str, memories: Iterable[EngineMemory], *, top_k: int = 20) -> list[RetrievalItem]:
    query_tokens = _tokens(query)
    scored: list[RetrievalItem] = []
    for memory in memories:
        memory_tokens = _tokens(memory.content) | {label.lower() for label in memory.labels}
        overlap = query_tokens & memory_tokens
        if not overlap:
            continue
        score = len(overlap) / max(1, len(query_tokens))
        scored.append(
            RetrievalItem(
                id=memory.id,
                source_id=memory.source_id or memory.id,
                content=memory.content,
                score=score,
            )
        )
    scored.sort(key=lambda item: (item.score, item.id), reverse=True)
    return scored[:top_k]


def recent_memory_retrieval(memories: list[EngineMemory], *, top_k: int = 20) -> list[RetrievalItem]:
    return [
        RetrievalItem(
            id=memory.id,
            source_id=memory.source_id or memory.id,
            content=memory.content,
            score=1.0,
        )
        for memory in memories[-top_k:]
    ]


def _claim_relation() -> EngineRelation:
    return EngineRelation("agent_decision", "audit_trail", "bridge", 0.82, False)


def _claim_memory(index: int, *, source_id: str, wording: str, prefix: str = "claim") -> EngineMemory:
    return EngineMemory(
        id=f"{prefix}_{index:02d}",
        content=wording,
        labels=["agent_decision", "audit_trail"],
        relations=[_claim_relation()],
        bridge_potential=0.82,
        importance=0.72,
        persistence=0.74,
        source_id=source_id,
    )


def _noise_memory(index: int, content: str, labels: list[str], prefix: str = "noise") -> EngineMemory:
    return EngineMemory(
        id=f"{prefix}_{index:02d}",
        content=content,
        labels=labels,
        relations=[],
        importance=0.35,
        persistence=0.30,
        source_id=f"{prefix}_source_{index:02d}",
    )


def same_source_dataset() -> list[EngineMemory]:
    paraphrases = [
        "The agent decision lacks an audit trail after deployment approval.",
        "Deployment approval happened, but the agent decision trail is still missing.",
        "We keep seeing agent decisions without a usable audit trail.",
        "The same deployment note repeats that agent decisions need traceable audit evidence.",
        "Agent decision review is blocked because the audit trail is incomplete.",
        "The approval record again mentions missing audit trail for agent decisions.",
        "Auditability remains weak around the agent decision process.",
        "A repeated report says agent decisions cannot be checked without an audit trail.",
    ]
    memories = [
        _claim_memory(index, source_id="incident_report_A", wording=wording, prefix="same_claim")
        for index, wording in enumerate(paraphrases)
    ]
    memories.extend(_shared_noise(prefix="same_noise"))
    return memories


def independent_source_dataset() -> list[EngineMemory]:
    independent = [
        ("security_review", "Security review found agent decisions without a traceable audit trail."),
        ("customer_ticket", "A customer ticket asks why the agent decision has no audit trail."),
        ("ops_postmortem", "The operations postmortem says audit trails are missing for agent decisions."),
        ("compliance_note", "Compliance notes require agent decision records to include audit trails."),
        ("qa_report", "QA found agent decision outputs that could not be audited."),
    ]
    memories = [
        _claim_memory(index, source_id=source, wording=wording, prefix="ind_claim")
        for index, (source, wording) in enumerate(independent)
    ]
    memories.extend(_shared_noise(prefix="ind_noise"))
    return memories


def mixed_context_dataset() -> list[EngineMemory]:
    same = same_source_dataset()[:5]
    independent = independent_source_dataset()[:3]
    memories = [
        _claim_memory(index, source_id="incident_report_A", wording=memory.content, prefix="mixed_same")
        for index, memory in enumerate(same)
    ]
    memories.extend(
        _claim_memory(index, source_id=memory.source_id or f"mixed_source_{index}", wording=memory.content, prefix="mixed_ind")
        for index, memory in enumerate(independent)
    )
    memories.extend(_shared_noise(prefix="mixed_noise"))
    memories.extend(
        [
            _noise_memory(30, "Audit logs for coffee machine maintenance are complete.", ["audit_log", "maintenance"], prefix="mixed_extra"),
            _noise_memory(31, "Deployment notes mention customer onboarding, not agent decisions.", ["deployment", "customer_onboarding"], prefix="mixed_extra"),
            _noise_memory(32, "A trail map for the company retreat was updated.", ["trail", "retreat"], prefix="mixed_extra"),
        ]
    )
    return memories


def _shared_noise(*, prefix: str) -> list[EngineMemory]:
    return [
        _noise_memory(1, "The cafeteria decision about coffee vendors has a clear paper trail.", ["coffee", "vendor_decision"], prefix=prefix),
        _noise_memory(2, "Deployment temperature checks were recorded in the maintenance log.", ["deployment", "maintenance_log"], prefix=prefix),
        _noise_memory(3, "The marketing agent selected images for a campaign audit.", ["marketing", "campaign_audit"], prefix=prefix),
        _noise_memory(4, "A hiking trail near the office was closed after rain.", ["hiking_trail", "weather"], prefix=prefix),
        _noise_memory(5, "Customer onboarding decisions are stored in a separate CRM workflow.", ["customer_onboarding", "crm"], prefix=prefix),
        _noise_memory(6, "Security badges were audited after the office move.", ["security_badge", "office_move"], prefix=prefix),
        _noise_memory(7, "The product roadmap changed after a leadership decision.", ["roadmap", "leadership"], prefix=prefix),
        _noise_memory(8, "The build agent failed because the cache directory was missing.", ["build_agent", "cache"], prefix=prefix),
    ]


def _engine_result(memories: list[EngineMemory]) -> object:
    return MemoryEngine().build_context(
        current_message="How broadly supported is the concern that agent decisions lack audit trails?",
        current_labels=["agent_decision", "audit_trail"],
        current_relations=[_claim_relation()],
        memories=memories,
    )


def _engine_after_keyword(memories: list[EngineMemory]) -> object:
    retrieved = keyword_overlap_retrieval("agent decision audit trail support", memories, top_k=12)
    selected_ids = {item.id for item in retrieved}
    selected = [memory for memory in memories if memory.id in selected_ids]
    return _engine_result(selected)


def _evaluate_case(name: str, memories: list[EngineMemory], *, expected_mode: str) -> ComparativeResult:
    start = perf_counter()
    query = "agent decision audit trail support"
    recent = recent_memory_retrieval(memories, top_k=12)
    keyword = keyword_overlap_retrieval(query, memories, top_k=12)
    engine = _engine_result(memories)
    keyword_so = _engine_after_keyword(memories)
    elapsed_ms = (perf_counter() - start) * 1000

    naive_keyword_support = len(keyword)
    keyword_unique_sources = len({item.source_id for item in keyword})
    engine_unique_sources = engine.evidence_summary.unique_source_count
    engine_contextual = engine.evidence_summary.contextual_recurrence_count
    keyword_so_unique_sources = keyword_so.evidence_summary.unique_source_count
    keyword_so_contextual = keyword_so.evidence_summary.contextual_recurrence_count

    checks: list[str] = []
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        if condition:
            checks.append(label)
        else:
            failures.append(label)

    check("keyword baseline retrieves some candidates", naive_keyword_support > 0)
    check("SO exposes contextual recurrence", engine_contextual >= 1)
    check("SO exposes unique source evidence", engine_unique_sources >= 1)

    if expected_mode == "same_source":
        check("same-source repetition is not treated as equal independent breadth", engine_unique_sources < engine_contextual)
        check("keyword support count is larger than keyword unique source count", naive_keyword_support > keyword_unique_sources)
    elif expected_mode == "independent_sources":
        check("independent-source case exposes broader source breadth", engine_unique_sources >= 5)
        check("source breadth is close to contextual recurrence", engine_unique_sources >= min(engine_contextual, 5))
    elif expected_mode == "mixed":
        check("mixed case preserves both recurrence and source breadth", engine_contextual > engine_unique_sources >= 4)
        check("keyword plus SO still separates evidence views", keyword_so_contextual >= keyword_so_unique_sources >= 2)

    metrics: dict[str, int | float | str] = {
        "memory_count": len(memories),
        "recent_support_count": len(recent),
        "recent_unique_source_count": len({item.source_id for item in recent}),
        "keyword_support_count": naive_keyword_support,
        "keyword_unique_source_count": keyword_unique_sources,
        "so_unique_source_count": engine_unique_sources,
        "so_contextual_recurrence_count": engine_contextual,
        "keyword_plus_so_unique_source_count": keyword_so_unique_sources,
        "keyword_plus_so_contextual_recurrence_count": keyword_so_contextual,
    }
    notes = [
        "This benchmark uses transparent keyword overlap, not real embeddings.",
        "It does not prove superiority over production vector retrieval.",
        "It tests whether evidence recurrence and source breadth remain distinguishable.",
    ]
    return ComparativeResult(
        name=name,
        passed=not failures,
        elapsed_ms=elapsed_ms,
        checks=checks,
        failures=failures,
        metrics=metrics,
        notes=notes,
    )


def run_comparative_benchmarks() -> list[ComparativeResult]:
    return [
        _evaluate_case("evidence_identity_same_source", same_source_dataset(), expected_mode="same_source"),
        _evaluate_case("evidence_identity_independent_sources", independent_source_dataset(), expected_mode="independent_sources"),
        _evaluate_case("evidence_identity_mixed_context", mixed_context_dataset(), expected_mode="mixed"),
    ]


def main() -> int:
    results = run_comparative_benchmarks()
    passed = sum(1 for result in results if result.passed)
    total = len(results)

    print("SO Memory Engine comparative benchmarks")
    print("=======================================")
    print()
    print("Scope: Evidence Identity")
    print("Baselines: recent memory, transparent keyword overlap, SO, keyword overlap + SO")
    print("Caution: no embeddings or LLM calls are used in this alpha comparison.")
    print()
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status} {result.name} ({result.elapsed_ms:.2f} ms)")
        for check in result.checks:
            print(f"  ok: {check}")
        for failure in result.failures:
            print(f"  fail: {failure}")
        print(
            "  metrics: "
            f"keyword_support={result.metrics['keyword_support_count']}, "
            f"keyword_sources={result.metrics['keyword_unique_source_count']}, "
            f"so_sources={result.metrics['so_unique_source_count']}, "
            f"so_contextual={result.metrics['so_contextual_recurrence_count']}"
        )
        print()

    output_dir = PROJECT_ROOT / "benchmark_results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "comparative_benchmarks.json"
    output_path.write_text(
        json.dumps([result.to_dict() for result in results], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"SO Memory Engine comparative benchmarks: {passed} passed, {total - passed} failed, {total} total")
    print(f"saved json: {output_path}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

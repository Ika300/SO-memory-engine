from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import sys
from time import perf_counter
from typing import Callable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "examples") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "examples"))

from evaluation_cases import (  # noqa: E402
    direction_preservation_case,
    independent_sources_case,
    noise_no_return_case,
    reactivation_case,
    same_source_repetition_case,
)
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine  # noqa: E402


@dataclass(slots=True)
class BenchmarkResult:
    name: str
    passed: bool
    elapsed_ms: float
    checks: list[str]
    failures: list[str]
    metrics: dict[str, int | float | str]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "passed": self.passed,
            "elapsed_ms": round(self.elapsed_ms, 3),
            "checks": list(self.checks),
            "failures": list(self.failures),
            "metrics": dict(self.metrics),
        }


def _run_case(name: str, runner: Callable[[], object], checks: list[tuple[str, Callable[[object], bool]]]) -> BenchmarkResult:
    start = perf_counter()
    result = runner()
    elapsed_ms = (perf_counter() - start) * 1000

    failures: list[str] = []
    passed_checks: list[str] = []
    for label, check in checks:
        if check(result):
            passed_checks.append(label)
        else:
            failures.append(label)

    evidence = result.evidence_summary
    metrics: dict[str, int | float | str] = {
        "active_memories": len(result.active_memories),
        "returning_memories": len(result.returning_memories),
        "recurring_structures": len(result.recurring_structures),
        "unresolved_tensions": len(result.unresolved_tensions),
        "structural_connections": len(result.structural_connections),
        "independent_fragment_count": evidence.independent_source_count,
        "unique_source_count": evidence.unique_source_count,
        "contextual_recurrence_count": evidence.contextual_recurrence_count,
    }
    return BenchmarkResult(
        name=name,
        passed=not failures,
        elapsed_ms=elapsed_ms,
        checks=passed_checks,
        failures=failures,
        metrics=metrics,
    )


def _scale_case() -> object:
    memories: list[EngineMemory] = []
    for index in range(30):
        if index % 3 == 0:
            labels = ["memory", "structure"]
            relations = [EngineRelation("memory", "structure", "bridge", 0.8, False)]
            bridge_potential = 0.8
        elif index % 3 == 1:
            labels = ["noise", f"control_{index}"]
            relations = []
            bridge_potential = 0.0
        else:
            labels = ["structure", "return"]
            relations = [EngineRelation("structure", "return", "support", 0.7, True)]
            bridge_potential = 0.0
        memories.append(
            EngineMemory(
                id=f"scale_{index:02d}",
                content=f"Synthetic memory fragment {index} for Engine scale benchmark.",
                labels=labels,
                relations=relations,
                bridge_potential=bridge_potential,
                source_id=f"source_{index:02d}",
            )
        )

    return MemoryEngine().build_context(
        current_message="Memory and structure return while unrelated controls remain separate.",
        current_labels=["memory", "structure", "return"],
        current_relations=[
            EngineRelation("memory", "structure", "bridge", 0.8, False),
            EngineRelation("structure", "return", "support", 0.7, True),
        ],
        memories=memories,
    )


def run_benchmarks() -> list[BenchmarkResult]:
    same_case = same_source_repetition_case()
    independent_case = independent_sources_case()
    reactivation = reactivation_case()
    noise = noise_no_return_case()
    direction = direction_preservation_case()

    return [
        _run_case(
            "same_source_repetition",
            same_case.run,
            [
                ("creates recurring structure", lambda r: len(r.recurring_structures) >= 1),
                ("keeps contextual recurrence", lambda r: r.evidence_summary.contextual_recurrence_count >= 1),
                ("does not inflate unique source count as independent evidence", lambda r: r.evidence_summary.unique_source_count == 2),
            ],
        ),
        _run_case(
            "independent_sources",
            independent_case.run,
            [
                ("creates recurring structure", lambda r: len(r.recurring_structures) >= 1),
                ("exposes independent source breadth", lambda r: r.evidence_summary.unique_source_count >= 3),
                ("activates supporting memories", lambda r: len(r.active_memories) >= 1),
            ],
        ),
        _run_case(
            "reactivation",
            reactivation.run,
            [
                ("returns prior memory", lambda r: len(r.returning_memories) >= 1),
                ("activates reactivated fragment", lambda r: any(m.fragment_id == "reactivation_past" for m in r.active_memories)),
            ],
        ),
        _run_case(
            "noise_no_return",
            noise.run,
            [
                ("does not create return from unrelated labels", lambda r: len(r.returning_memories) == 0),
                ("does not activate unrelated memories", lambda r: len(r.active_memories) == 0),
                ("does not guess semantic similarity", lambda r: len(r.structural_connections) == 0),
            ],
        ),
        _run_case(
            "direction_preservation",
            direction.run,
            [
                ("does not collapse reversed directed relation", lambda r: len(r.returning_memories) == 0),
                ("does not activate reversed-direction memory", lambda r: len(r.active_memories) == 0),
            ],
        ),
        _run_case(
            "mixed_scale_30_fragments",
            _scale_case,
            [
                ("runs mixed 30-fragment case", lambda r: r.context_pack.current_message.startswith("Memory and structure")),
                ("keeps structural signal visible", lambda r: len(r.recurring_structures) >= 1),
                ("keeps evidence breadth visible", lambda r: r.evidence_summary.unique_source_count >= 10),
            ],
        ),
    ]


def main() -> int:
    results = run_benchmarks()
    passed = sum(1 for result in results if result.passed)
    total = len(results)

    print("SO Memory Engine benchmarks")
    print("===========================")
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
            f"active={result.metrics['active_memories']}, "
            f"returning={result.metrics['returning_memories']}, "
            f"recurring={result.metrics['recurring_structures']}, "
            f"unique_sources={result.metrics['unique_source_count']}, "
            f"contextual={result.metrics['contextual_recurrence_count']}"
        )
        print()

    output_dir = PROJECT_ROOT / "benchmark_results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "engine_benchmarks.json"
    output_path.write_text(
        json.dumps([result.to_dict() for result in results], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"SO Memory Engine benchmarks: {passed} passed, {total - passed} failed, {total} total")
    print(f"saved json: {output_path}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

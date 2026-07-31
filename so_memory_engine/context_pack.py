from __future__ import annotations

from collections import defaultdict

from .models import (
    ActiveMemory,
    ContextPack,
    EngineMemory,
    EvidenceSummary,
    RecurringStructure,
    StructuralConnection,
    UnresolvedTension,
)


def build_evidence_summary(kernel_result, memories: list[EngineMemory]) -> EvidenceSummary:
    """Build Engine-level evidence summary from available Kernel traces.

    Kernel EvidenceIdentity is Insight-oriented. Engine context should still
    expose evidence history when Insight JSON is not created, so this function
    safely falls back to Pattern Identity groups without changing Core behavior.
    """

    evidence = kernel_result.evidence_identity
    independent_fragment_ids = list(evidence.independent_source_fragment_ids)
    contextual_overlay_ids = list(evidence.contextual_recurrence_overlay_ids)

    for group in kernel_result.pattern_identity_groups:
        for fragment_id in group.source_fragment_ids:
            if fragment_id not in independent_fragment_ids:
                independent_fragment_ids.append(fragment_id)
        for overlay_id in group.contextual_recurrence_overlay_ids:
            if overlay_id not in contextual_overlay_ids:
                contextual_overlay_ids.append(overlay_id)

    memory_by_id = {memory.id: memory for memory in memories}
    unique_source_ids: list[str] = []
    for fragment_id in independent_fragment_ids:
        memory = memory_by_id.get(fragment_id)
        source_id = memory.source_id if memory and memory.source_id else fragment_id
        if source_id not in unique_source_ids:
            unique_source_ids.append(source_id)

    trace_count = max(evidence.independent_source_count, len(independent_fragment_ids))
    contextual_count = max(evidence.contextual_recurrence_count, len(contextual_overlay_ids))
    return EvidenceSummary(
        trace_fragment_count=trace_count,
        contextual_recurrence_count=contextual_count,
        independent_source_fragment_ids=independent_fragment_ids,
        contextual_recurrence_overlay_ids=contextual_overlay_ids,
        unique_source_ids=unique_source_ids,
    )


def build_recurring_structures(kernel_result) -> list[RecurringStructure]:
    structures: list[RecurringStructure] = []
    for group in kernel_result.pattern_identity_groups:
        if group.occurrence_count < 2:
            continue
        structures.append(
            RecurringStructure(
                identity_key=group.identity_key,
                pattern_type=group.pattern_type,
                center_candidate=group.center_candidate,
                member_nodes=list(group.member_nodes),
                occurrence_count=group.occurrence_count,
                trace_fragment_count=group.independent_source_count,
                contextual_recurrence_count=group.contextual_recurrence_count,
                source_fragment_ids=list(group.source_fragment_ids),
            )
        )
    structures.sort(
        key=lambda item: (
            item.occurrence_count,
            item.trace_fragment_count,
            item.contextual_recurrence_count,
        ),
        reverse=True,
    )
    return structures


def build_unresolved_tensions(kernel_result) -> list[UnresolvedTension]:
    tensions: list[UnresolvedTension] = []
    for group in kernel_result.pattern_identity_groups:
        if group.pattern_type != "Tension":
            continue
        tensions.append(
            UnresolvedTension(
                label=group.center_candidate or "tension",
                member_nodes=list(group.member_nodes),
                source_fragment_ids=list(group.source_fragment_ids),
                occurrence_count=group.occurrence_count,
            )
        )
    tensions.sort(key=lambda item: (item.occurrence_count, len(item.source_fragment_ids)), reverse=True)
    return tensions


def build_structural_connections(kernel_result) -> list[StructuralConnection]:
    connections: list[StructuralConnection] = []
    for group in kernel_result.pattern_identity_groups:
        if group.pattern_type not in {"Bridge", "Chain", "Star"}:
            continue
        connections.append(
            StructuralConnection(
                label=group.center_candidate or group.pattern_type.lower(),
                member_nodes=list(group.member_nodes),
                source_fragment_ids=list(group.source_fragment_ids),
                occurrence_count=group.occurrence_count,
            )
        )
    connections.sort(key=lambda item: (item.occurrence_count, len(item.source_fragment_ids)), reverse=True)
    return connections


def build_active_memories(
    memories: list[EngineMemory],
    kernel_result,
) -> list[ActiveMemory]:
    memory_by_id = {memory.id: memory for memory in memories}
    reasons_by_fragment: dict[str, list[str]] = defaultdict(list)
    keys_by_fragment: dict[str, list[str]] = defaultdict(list)

    for candidate in kernel_result.return_candidates:
        for fragment_id in candidate.past_fragment_ids:
            reasons_by_fragment[fragment_id].append("reactivated by current structure")
            for key in candidate.shared_pattern_identity_keys:
                if key not in keys_by_fragment[fragment_id]:
                    keys_by_fragment[fragment_id].append(key)

    for group in kernel_result.pattern_identity_groups:
        if group.occurrence_count < 2:
            continue
        for fragment_id in group.source_fragment_ids:
            if fragment_id == "current":
                continue
            reasons_by_fragment[fragment_id].append(
                f"supports recurring {group.pattern_type} structure"
            )
            if group.identity_key not in keys_by_fragment[fragment_id]:
                keys_by_fragment[fragment_id].append(group.identity_key)

    active: list[ActiveMemory] = []
    for fragment_id, reasons in reasons_by_fragment.items():
        memory = memory_by_id.get(fragment_id)
        if memory is None:
            continue
        deduped_reasons = []
        for reason in reasons:
            if reason not in deduped_reasons:
                deduped_reasons.append(reason)
        active.append(
            ActiveMemory(
                fragment_id=fragment_id,
                content=memory.content,
                labels=list(memory.labels),
                activation_reason="; ".join(deduped_reasons),
                pattern_identity_keys=keys_by_fragment[fragment_id],
            )
        )
    active.sort(key=lambda item: (len(item.pattern_identity_keys), item.fragment_id), reverse=True)
    return active


def build_context_pack(current_message: str, memories: list[EngineMemory], kernel_result) -> ContextPack:
    evidence_summary = build_evidence_summary(kernel_result, memories)
    recurring_structures = build_recurring_structures(kernel_result)
    unresolved_tensions = build_unresolved_tensions(kernel_result)
    structural_connections = build_structural_connections(kernel_result)
    active_memories = build_active_memories(memories, kernel_result)
    return ContextPack(
        current_message=current_message,
        active_memories=active_memories,
        returning_memories=list(kernel_result.return_candidates),
        recurring_structures=recurring_structures,
        unresolved_tensions=unresolved_tensions,
        structural_connections=structural_connections,
        evidence_summary=evidence_summary,
    )

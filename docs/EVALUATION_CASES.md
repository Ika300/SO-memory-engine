# Evaluation Cases

SO Memory Engine evaluation cases define what the Engine should and should not do.

They are not LLM evaluations. They are deterministic structural-memory checks.

Run:

```bash
py -3 examples\run_evaluation_cases.py
py -3 -m unittest discover -s tests -p '*test*.py' -v
```

The runner saves JSON and text outputs under `outputs/`.

## Evidence counts

The Engine exposes two evidence-width views:

- `trace_fragment_count`: fragment-level evidence breadth from Kernel traces
- `unique_source_count`: Engine-level source-id breadth using `EngineMemory.source_id`

The current fragment is also counted as a current source when it participates in a structure.

This means same-source repetition and multi-source evidence can have similar recurrence while still differing in source-id breadth.

## Case 1: same_source_repetition

Purpose:

A single source repeats the same structure across memory fragments.

What it checks:

- recurring structure appears
- contextual recurrence appears
- repetition is preserved, not suppressed

Why it matters:

AI memory should not treat repeated exposure as meaningless noise. Repetition can matter. But it should remain distinguishable from broad independent evidence.

## Case 2: independent_sources

Purpose:

Different source origins supply the same structural bridge.

What it checks:

- multiple memories can support the same structure
- active memories can be produced from repeated structural identity
- source breadth remains visible

Why it matters:

Many independent origins should not be collapsed into one vague memory. The Engine should expose that separate evidence exists.

## Case 3: reactivation

Purpose:

The current message reactivates a prior exact structural identity.

What it checks:

- Return candidates are produced
- prior memory becomes active
- current structure can touch past structure without semantic guessing

Why it matters:

This is one of the Engine's core behaviors. It observes what returns.

## Case 4: noise_no_return

Purpose:

Unrelated labels should not create Return candidates by semantic guessing.

What it checks:

- no Return candidates
- no active memories
- no hidden semantic dictionary

Why it matters:

The Engine must not pretend unrelated memories are relevant just because an AI-like system could invent an interpretation.

## Case 5: direction_preservation

Purpose:

Reversed directed relations should not collapse into the same structural identity.

What it checks:

- reversed direction does not create exact Return
- active memories are not produced from directionally different structure

Why it matters:

Direction is part of structure. `memory -> structure` and `structure -> memory` are not automatically the same event.

## Evaluation boundary

These cases are intentionally small.

They do not test:

- natural language parsing
- semantic similarity
- LLM response quality
- storage
- UI
- cloud behavior

They test the Engine's structural memory boundary.

## Current interpretation

If these cases pass, the Engine can currently claim:

- it can build Context Packs from current input and past memories
- it can surface returning structures
- it can expose recurring structures
- it can avoid semantic guessing in unrelated cases
- it preserves direction-sensitive structure
- it remains LLM-free and local

It should not yet claim:

- full production readiness
- automatic natural-language understanding
- complete AI memory replacement
- SaaS readiness

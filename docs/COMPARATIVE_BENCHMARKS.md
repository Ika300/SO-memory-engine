# Comparative Benchmarks

Comparative benchmarks test whether SO Memory Engine exposes a memory distinction that simpler context methods can blur.

The current alpha comparative benchmark focuses on Evidence Identity.

## Scope

Question:

> How broadly supported is the concern that agent decisions lack audit trails?

The benchmark compares:

- recent memory
- transparent keyword overlap
- SO Memory Engine
- keyword overlap plus SO Memory Engine

No LLM calls, embeddings, external APIs, vector databases, or hidden semantic dictionaries are used.

This is intentional. The first comparison should be inspectable and reproducible before adding heavier dependencies.

## What it measures

The benchmark checks whether the system keeps these two quantities separate:

- **unique source evidence** — how many distinct source origins support the structure?
- **contextual recurrence** — how many structural contexts repeatedly expose the structure?

These are not the same thing.

Repeated appearances from one source may create high contextual recurrence without broad independent support. Multiple independent sources may create broader source evidence even if recurrence is lower.

## Current cases

### evidence_identity_same_source

Repeated paraphrases of the same concern come from one source, mixed with similar and unrelated noise.

Expected behavior:

- keyword overlap retrieves many apparently relevant candidates
- SO preserves recurrence
- SO does not treat repeated same-source material as broad independent evidence

### evidence_identity_independent_sources

The same structure appears across several independent sources, mixed with noise.

Expected behavior:

- SO exposes broader unique source evidence
- contextual recurrence and source breadth remain distinguishable

### evidence_identity_mixed_context

Same-source repetition and independent sources appear together with noise.

Expected behavior:

- SO preserves both recurrence and source breadth
- keyword overlap plus SO still separates evidence views

## Run

From `SO_Memory_Engine`:

```bash
py -3 benchmarks\run_comparative_benchmarks.py
```

On non-Windows systems:

```bash
python benchmarks/run_comparative_benchmarks.py
```

The runner writes JSON output to:

```text
benchmark_results/comparative_benchmarks.json
```

`benchmark_results/` is ignored by Git.

## Current measured result

```text
Comparative benchmarks: 3/3 passed
External API calls: 0
Embeddings required: No
LLM required: No
```

This measured result should be updated only after rerunning the benchmark.

## What this does not prove

This benchmark does not prove:

- superiority over production embedding retrieval
- superiority over all RAG systems
- natural-language extraction accuracy
- production-scale performance
- that SO should replace vector retrieval

It only shows that, given structured memory fragments, SO Memory Engine can keep source breadth and contextual recurrence distinct in the included Evidence Identity cases.

## Why this benchmark matters

A naive memory system may see repeated similar fragments and treat them as many supporting pieces of evidence.

SO Memory Engine is designed to preserve a different view:

```text
Same source seen many times != many independent sources
```

This is the first practical benchmark because it is easy to inspect and directly connected to AI memory reliability.

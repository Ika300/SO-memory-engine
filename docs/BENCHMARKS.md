# Engine Benchmarks

SO Memory Engine benchmarks are behavioral benchmarks.

They are designed to answer:

> Does the Engine still preserve the memory behaviors that make it different from ordinary similarity retrieval?

They are not primarily speed contests. Elapsed time is reported, but pass/fail is based on structural behavior.

## Run

From `SO_Memory_Engine`:

```bash
py -3 benchmarks\run_benchmarks.py
```

The runner writes JSON output to:

```text
benchmark_results/engine_benchmarks.json
```

`benchmark_results/` is ignored by Git.

## Current benchmark cases

### same_source_repetition

Checks that repeated structure from one source creates recurrence without pretending to be many independent sources.

### independent_sources

Checks that the same structure from different source origins exposes broader source evidence.

### reactivation

Checks that a current structure can reactivate a prior exact structural identity.

### noise_no_return

Checks that unrelated labels do not create Return candidates by semantic guessing.

### direction_preservation

Checks that reversed directed relations do not collapse into the same structural identity.

### mixed_scale_30_fragments

Checks that a small mixed memory set runs successfully while preserving signal, noise separation, and evidence breadth.

## What is measured

Each case reports:

- active memories
- returning memories
- recurring structures
- unresolved tensions
- structural connections
- independent fragment count
- unique source count
- contextual recurrence count
- elapsed milliseconds

## Design boundary

Benchmarks must not add:

- LLM calls
- embeddings
- semantic dictionaries
- fuzzy semantic merging
- storage requirements
- UI assumptions

The benchmark should test the Engine as a structural memory context layer.

# Benchmark Strategy

SO Memory Engine should not be benchmarked as a vector database.

It is not trying to win on embedding similarity, approximate nearest-neighbor speed, or top-k retrieval latency. Those are important problems, but they are not the Engine's main claim.

The Engine should be benchmarked as a structural context construction layer for AI memory.

## Core claim

Vector memory retrieves what is similar.  
SO Memory Engine observes what returns.

The benchmark suite should therefore measure whether the Engine preserves structural memory properties that ordinary similarity retrieval tends to blur.

## Five benchmark pillars

### 1. Structure Recurrence

Can the Engine detect that the same structure has returned across different memory fragments?

This should not require identical text. The caller supplies structure, and the Engine checks whether structural identity recurs.

Current coverage:

- `same_source_repetition`
- `mixed_scale_30_fragments`

### 2. Evidence Independence

Can the Engine distinguish repeated exposure to the same source from multiple independent source origins?

This matters because seeing the same evidence many times is not the same as seeing many independent evidences.

Current coverage:

- `same_source_repetition`
- `independent_sources`

### 3. Structural Return

Can a current input reactivate a past structural identity?

The goal is not to retrieve the most similar old text. The goal is to expose a past structure that has become relevant again.

Current coverage:

- `reactivation`

### 4. Conflict and Tension Discovery

Can the Engine preserve unresolved tensions without pretending to resolve them?

This is important for AI agents because long-term memory often contains changing goals, constraints, conflicts, or tradeoffs.

Current coverage:

- tension-related fields in evaluation cases
- future benchmark expansion needed

### 5. Noise Rejection

Can the Engine avoid activating unrelated memories by semantic guessing?

This is central to the project. The Engine should not invent meaning or merge concepts by hidden dictionary.

Current coverage:

- `noise_no_return`
- `direction_preservation`

## Secondary measurements

The benchmark runner also reports:

- active memories
- returning memories
- recurring structures
- unresolved tensions
- structural connections
- independent fragment count
- unique source count
- contextual recurrence count
- elapsed milliseconds

Elapsed time is useful, but it is not the primary benchmark claim.

## Future benchmark work

Future benchmark work should add:

- Context Pack utility tests
- Context compression measurements
- stronger conflict/tension cases
- current-state reconstruction experiments
- optional comparisons with naive recent memory, keyword search, vector search, and long context

These should be added only when they can be measured honestly.

## What not to benchmark as the main claim

Do not lead with:

- vector search speed
- embedding similarity accuracy
- million-scale ANN latency
- generic RAG top-k retrieval

Those benchmarks pull the project onto the wrong battlefield.

## Good public framing

A good public benchmark question is:

> Given structured memory fragments, can SO Memory Engine build a compact Context Pack that preserves recurrence, return, evidence identity, unresolved tension, and noise rejection?

That is the Engine's real arena.

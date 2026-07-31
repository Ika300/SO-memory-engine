# Benchmark Strategy

SO Memory Engine should not be benchmarked as a vector database.

It is not trying to win on embedding similarity, approximate nearest-neighbor speed, or top-k retrieval latency. Those are important problems, but they are not the Engine's main claim.

The Engine should be benchmarked as a structural context construction layer for AI memory.

## Core claim

Vector memory retrieves what is similar.  
SO Memory Engine observes what returns.

A practical system can also combine them:

```text
Vector retrieval finds candidates.
SO reconstructs structural context.
```

This means SO can sit after keyword, metadata, or vector retrieval. It does not need to replace them.

## Two benchmark layers

### 1. Behavioral benchmarks

Behavioral benchmarks test whether the Engine preserves its own intended memory behaviors.

They answer:

> Given structured memory fragments, does the Engine preserve recurrence, return, evidence identity, unresolved tension, directionality, and noise rejection?

Current measured status:

```text
Behavioral benchmarks: 6/6 passed
Engine tests: 31/31 passed
External API calls: 0
Embeddings required: No
LLM required: No
```

These numbers should be updated only after rerunning the suite.

### 2. Comparative application benchmarks

Comparative benchmarks have started with a narrow Evidence Identity comparison. Broader application benchmarks are future work.

Comparative benchmarks should test whether an AI application performs better when SO Memory Engine is used as part of its memory pipeline.

Potential baselines:

- no memory
- recent memory
- keyword search
- simple similarity retrieval
- embedding retrieval
- SO Memory Engine
- embedding retrieval plus SO

Additional comparisons should be added only when they can be measured honestly.

## Five behavioral benchmark pillars

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

### 4. Conflict and Tension Preservation

Can the Engine preserve unresolved tensions without pretending to resolve them?

This is important for AI agents because long-term memory often contains changing goals, constraints, conflicts, or tradeoffs.

Current coverage:

- tension-related fields in evaluation cases
- future benchmark expansion needed

### 5. Noise Rejection and Direction Preservation

Can the Engine avoid activating unrelated memories by semantic guessing?

Can it preserve directed relations instead of collapsing reversed structure into the same identity?

This is central to the project. The Engine should not invent meaning or merge concepts by hidden dictionary.

Current coverage:

- `noise_no_return`
- `direction_preservation`

## First recommended comparative experiment

The first comparative experiment focuses on Evidence Identity and is implemented in `benchmarks/run_comparative_benchmarks.py`.

Question:

> How broadly supported is this recurring concern?

Dataset shape:

- same-source paraphrases
- independent sources
- similar but irrelevant noise
- different wording with the same structure
- unrelated noise

Expected comparison target:

```text
Naive similarity retrieval:
Repeated paraphrases may look like multiple pieces of evidence.

SO Memory Engine:
Contextual recurrence and independent source evidence remain separate.

Embedding retrieval + SO:
Retrieval narrows candidates; SO reconstructs evidence structure.
```

This benchmark should be built to reveal both strengths and limits. It should not be tuned only to make SO win.

## Secondary measurements

The benchmark runner also reports:

- active memories
- returning memories
- recurring structures
- unresolved tensions
- structural connections
- trace fragment count
- unique source count
- contextual recurrence count
- elapsed milliseconds

Elapsed time is useful, but it is not the primary benchmark claim.

## What not to benchmark as the main claim

Do not lead with:

- vector search speed
- embedding similarity accuracy
- million-scale ANN latency
- generic RAG top-k retrieval

Those benchmarks pull the project onto the wrong battlefield.

## What current benchmarks do not prove

Current behavioral benchmarks do not prove:

- universal improvement for all AI apps
- superiority over every retrieval system
- production-scale performance
- natural-language extraction accuracy
- automatic understanding of arbitrary raw text

They prove that the alpha Engine preserves its intended structural memory behaviors on the included cases.



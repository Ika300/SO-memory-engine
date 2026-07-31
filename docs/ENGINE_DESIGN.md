# SO Memory Engine Design

## Objective

SO Memory Engine is an AI-app-facing memory layer built on SO Memory Kernel.

Its job is to prepare structured memory context for an LLM application without turning memory into approximate similarity search.

## Core sentence

Vector memory retrieves what is similar.
SO Memory Engine observes what returns.

## Inputs

The Engine accepts:

- current message
- current structural labels supplied by the caller
- current structural relations supplied by the caller
- past memory fragments supplied by the caller

The Engine may accept raw text as trace content, but it must not infer hidden long-term memory from it.

## Outputs

The Engine returns:

- active memories
- returning memories
- recurring structures
- unresolved tensions
- structural connections
- evidence summary
- Context Pack for LLM use
- raw Kernel result for traceability

## What the Engine does

The Engine:

1. converts caller-supplied current input into a current MemoryFragment
2. combines current and past fragments
3. calls SO Memory Kernel
4. reads Kernel output
5. builds a compact Context Pack
6. preserves traceability back to fragment ids

## What the Engine must not do

The Engine must not:

- modify Spiral Orbit Core
- change formulas, thresholds, Pattern types, or pipeline structure
- infer labels from natural language using a hidden dictionary
- use fuzzy semantic merging
- call an LLM
- summarize user history as fact
- decide what a user really means

## Why this exists

Most AI memory systems start with similarity:

- what old text is closest to the current input?

SO Memory Engine asks a different question:

- what structure is returning?
- what relation is recurring?
- what tension remains unresolved?
- what evidence is independent?
- what evidence is merely repeated context?

## v0.1 boundary

v0.1 is intentionally small.

It builds a Context Pack from existing SO Memory Kernel output.
Natural language parsing, storage, UI, cloud sync, and LLM response generation are outside scope.

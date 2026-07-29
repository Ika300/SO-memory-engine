# Kernel / Engine Boundary

## Kernel

SO Memory Kernel is the low-level structural memory SDK.

It owns:

- MemoryFragment
- MemoryRelation
- MemoryKernel
- Evidence Identity
- Pattern Identity
- Return / re-activation
- copied Spiral Orbit Core execution

The Kernel should remain strict, traceable, and non-semantic.

## Engine

SO Memory Engine is an application-facing layer above the Kernel.

It owns:

- current-message wrapping
- memory context construction
- active memory selection
- Context Pack formatting
- AI-app integration examples

## Boundary rule

Kernel observes structure.
Engine prepares usable context.
LLM generates language.

## Prohibited boundary violations

The Engine must not:

- reach into Spiral Orbit Core internals
- mutate Kernel output
- invent semantic labels
- merge structurally different memories because they sound similar
- replace the caller's parser or storage layer

The Kernel must not:

- become a chat application
- become a prompt system
- become a storage system
- depend on LLM output

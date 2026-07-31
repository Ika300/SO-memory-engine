# Integration Guide

SO Memory Engine is designed to sit between an application's memory store and its response generator.

It is intentionally narrow: it prepares structural memory context. It does not own storage, retrieval UX, natural-language parsing, or final response generation.

## Recommended integration shape

```text
Your app
  ↓
load current-space memories
  ↓
convert them into EngineMemory objects
  ↓
call MemoryEngine.build_context(...)
  ↓
pass ContextPack to your LLM as optional reference
  ↓
render or store the final response in your app
```

## What your app must provide

Your app is responsible for:

- choosing which memories to pass in
- assigning memory ids
- assigning source ids if source-level evidence matters
- supplying labels and relations if you have them
- storing messages and outputs
- deciding how the final LLM response is written

## What the Engine provides

The Engine provides:

- active memory candidates
- returning structure candidates
- recurring structural identities
- unresolved tension candidates
- structural connection candidates
- independent-source and contextual-recurrence evidence views
- a Context Pack suitable for LLM reference

## Important boundary

Do not treat Engine output as a finished interpretation of the user.

Engine output is structural memory context. It says, in effect:

> These prior fragments are structurally relevant.  
> These patterns returned.  
> This evidence appears in these sources or contexts.  
> Use cautiously.

The LLM or application layer should still decide how, whether, and when to use that context.

## No semantic dictionary

The Engine does not contain a hidden concept dictionary. It will not decide that two different words mean the same thing.

If your app wants labels, supply them explicitly. If labels are omitted, content is preserved as a single anchor by the underlying Kernel adapter.

This preserves the main design choice:

> do not flatten meaning by approximate semantic merging.

## Evidence identity

When using the Engine for AI memory, `source_id` is important.

Example:

- Ten fragments from one original note may mean strong contextual recurrence.
- Ten fragments from ten independent notes may mean stronger source breadth.

The Engine preserves these views:

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `independent_source_count` | Kernel trace fragment breadth. | Shows how much Kernel-level trace support exists. |
| `unique_source_count` | Caller-level unique `source_id` breadth. | Shows how many caller-defined sources contributed. |
| `contextual_recurrence_count` | Repeated overlay/context exposure. | Shows how often a structure was encountered across contexts. |

The current alpha name `independent_source_count` can be read as fragment-level trace breadth. If you need caller-level source breadth, use `unique_source_count`.

## Prompt usage

`ContextPack.to_prompt_text()` is intentionally direct and structural. It is best used as hidden or developer-side reference, not as text shown directly to end users.

A response generator should treat it as optional grounding:

- use it when it helps answer the current message
- do not expose internal labels unless useful
- do not invent user history
- do not turn candidates into facts

## Minimal production checklist

Before using the Engine inside a real AI app, decide:

- where memories are stored
- who assigns labels and relations
- how much memory is passed per request
- whether `source_id` represents message id, document id, session id, or author id
- how Context Pack output is hidden from the user
- how validation errors are handled

## Current non-goals

The Engine does not currently provide:

- database storage
- semantic embeddings
- web API
- authentication
- UI
- LLM calls
- natural-language parsing
- cloud sync

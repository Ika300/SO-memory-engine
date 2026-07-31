# SO Platform Product Strategy

This document fixes the product boundary for SO Memory Engine, SO Extractor, and future SO Extractor Pro work.

The purpose is to prevent the platform from becoming a mixed pile of Engine logic, extraction logic, parser research, sales promises, and LLM prompt templates.

## 1. Core platform shape

SO should be treated as a layered platform, not a single product.

```text
Raw conversation / notes / documents
        -> SO Extractor Free or Pro
        -> Structured Memory / MemoryUnit
        -> SO Memory Engine OSS
        -> Context Pack
        -> LLM / AI application
```

The layers have different jobs.

- Extractor: turns raw input into structured memory.
- Engine: observes structure, recurrence, return, connection, tension, and evidence identity.
- Context Pack: prepares Engine output as reference context.
- LLM / application: generates language, UX, decisions, or actions.

## 2. Strategic principle

The Engine should remain open.

The commercial value should come from producing better Engine-ready memory, not from hiding the Engine.

```text
Free value:
Use the Engine and understand the SO memory model.

Paid value:
Turn messy real logs into higher-quality SO-ready memory.
```

This avoids the weak open-core pattern where the free version is intentionally crippled. The free Engine should be real. The paid product should improve input quality, validation, evidence retention, and production integration.

## 3. Engine responsibility

SO Memory Engine is responsible for observing caller-supplied structure.

It should continue to provide:

- active memories
- returning memories
- recurring structures
- unresolved tensions
- structural connections
- evidence identity
- Context Pack output
- traceability into Kernel output

It should not become:

- a natural-language parser
- a chatbot
- a vector database
- a storage layer
- a UI
- a production extractor
- a hidden semantic dictionary
- a fuzzy semantic merge system

The Engine begins after structure exists.

## 4. Extractor responsibility

SO Extractor is responsible for producing structured memory from raw input.

Inputs may include:

- conversation logs
- ChatGPT exports
- agent traces
- notes
- documents
- meeting transcripts
- emails or Slack-like messages

Outputs should be Engine-ready or Engine-exportable structures, such as:

- MemoryUnit
- labels
- relations
- source_id
- source spans when available
- metadata
- confidence or extraction quality notes
- validation report

Extractor must not perform SO Engine observation. It prepares input. The Engine observes structure.

## 5. Free Extractor scope

Free Extractor should make SO Memory Engine usable by people who do not already have structured memory.

Free Extractor may use existing OSS tools, rule-based examples, simple schemas, and LLM structured-output templates.

Free Extractor should include:

- public MemoryUnit schema
- basic conversation loader
- simple rule-based extractor sample
- LLM structured-output prompt examples
- Pydantic-style validation model or equivalent schema validation
- EngineMemory exporter
- end-to-end demo into SO Memory Engine
- clear limitations

Free Extractor should not claim high extraction quality. It should be an entry point, not the commercial core.

## 6. Pro Extractor scope

SO Extractor Pro should be a commercial structuring and validation kit.

Its job is:

```text
Raw logs
    -> better MemoryUnits
    -> canonical memory candidates
    -> validation and quality reports
    -> Engine-ready output
```

Pro value should come from:

- better relation extraction
- more stable labels
- source/span/evidence preservation
- canonical memory candidates
- advanced validation
- extraction quality reports
- Engine-readiness reports
- repair hints
- production templates

Pro should not sell itself as perfect natural-language understanding.

## 7. SO Structural Parser long-term role

SO Structural Parser is the long-term commercial core candidate.

It is not merely an LLM prompt wrapper. It should gradually become a structural parser that turns language, traces, or documents into SO-friendly memory units.

Long-term target:

```text
Conversation
    -> SO Structural Parser
    -> MemoryUnit
    -> SO Memory Engine
```

The parser can be developed gradually. It does not need to be complete in Pro v0.1.

## 8. OSS extraction tools policy

Existing OSS extraction tools may be useful in Free Extractor and as Pro-side comparison or fallback.

Before adopting any specific tool, verify:

- the tool exists and is maintained
- license terms
- commercial-use rights
- dependency risk
- output stability
- whether it requires external APIs
- whether it can preserve source spans

Do not build product claims on unverified assumptions about an OSS tool.

Free Extractor may use OSS as the main extraction path.

Pro Extractor may use OSS as:

- bootstrap teacher
- comparison baseline
- fallback
- validation counterpart

But Pro value should not be merely:

```text
OSS extractor + prompt template
```

## 9. Canonical Memory principle

Canonical Memory is potentially the strongest paid feature, but also the most dangerous.

Bad canonicalization:

```text
similar meanings -> one flattened memory
```

This repeats the approximate-merge problem SO is designed to avoid.

Good canonicalization:

```text
multiple fragments appear to gather around one structural candidate
    -> keep canonical candidate
    -> keep all evidence
    -> keep source_id
    -> keep spans when available
    -> keep uncertainty
    -> do not erase original fragments
```

Canonical Memory must be treated as a candidate with evidence, not as a replacement for the original memory fragments.

## 10. No approximate semantic merge rule

SO products should not collapse meanings just because they are similar.

Allowed:

- grouping with evidence
- candidate canonicalization
- explicit relation mapping
- source-preserving normalization
- user-reviewable merge suggestions

Not allowed:

- hidden ontology merge
- silent synonym collapse
- deleting original evidence
- treating repeated phrasing as independent support
- claiming certainty when extraction is uncertain

## 11. Source, span, and evidence retention

Extractor Pro must preserve traceability.

At minimum, each extracted unit should retain:

- source_id
- conversation_id or document_id when available
- message_id when available
- role or speaker when available
- original text reference or span when available
- extraction method
- confidence or validation notes

For Pro, span-level traceability is a key differentiator.

Possible span levels:

- message
- sentence
- clause
- phrase
- character span

The paid feature is not just better extraction. It is safer extraction because the user can return to the evidence.

## 12. Free vs Pro boundary

| Area | Free Extractor | Extractor Pro |
| --- | --- | --- |
| Engine | Same OSS Engine | Same OSS Engine |
| Extraction path | OSS / rules / LLM templates | SO Structural Parser as main path |
| Schema | Public basic schema | Public schema plus commercial extensions |
| Validation | Basic validation | Advanced validation and repair hints |
| Relations | Simple relation candidates | Higher-quality relation extraction |
| Labels | LLM/OSS/rule dependent | Label stabilization and normalization |
| Source retention | Message-level | Message / sentence / clause / span |
| Canonical memory | None or minimal examples | Canonical Memory candidates with evidence |
| Reports | Basic error report | Extraction quality and Engine-readiness reports |
| Purpose | Let anyone try SO Engine | Make real logs useful for SO Engine |

## 13. Pro v0.1 target

Pro v0.1 should not attempt to be a perfect parser.

A realistic Pro v0.1 target is:

```text
Conversation Log Structuring + Validation + Canonical Memory Candidate Kit
```

Expected outputs:

- engine_memories.json
- memory_units.json
- canonical_memory_candidates.json
- validation_report.md
- engine_readiness_report.md
- context_pack_preview.txt

## 14. Pro v0.1 non-goals

Do not promise:

- perfect natural-language understanding
- fully autonomous memory extraction
- universal domain support
- replacement for all RAG systems
- replacement for human review
- hidden semantic correction
- complete independence from LLMs in early versions

## 15. Development roadmap

### Phase 1: Strategy fixed

- Keep Engine OSS.
- Define Free Extractor and Pro Extractor boundaries.
- Define Canonical Memory principles.
- Define no approximate merge rule.

### Phase 2: Free Extractor MVP

- Create a small `so-extractor` project.
- Add basic schema, loader, rule extractor, validator, exporter, and Engine demo.
- Keep it honest and limited.

### Phase 3: Pro specification

- Write `SO_EXTRACTOR_PRO_SPEC.md`.
- Define commercial outputs, reports, validation rules, packaging, and support boundaries.

### Phase 4: Pro MVP

- Build local conversion and validation kit.
- Add canonical memory candidates with evidence retention.
- Add Engine-readiness report.

### Phase 5: Comparative evaluation

Compare Free Extractor and Pro Extractor on:

- validation error rate
- source retention
- span retention
- relation endpoint validity
- label stability
- canonical candidate usefulness
- Engine activation quality
- Context Pack usefulness

### Phase 6: Sales package

Package Pro as a developer-facing integration kit, not as a vague AI product.

## 16. Sales position

Possible clear positioning:

```text
Turn raw AI conversation logs into SO Engine-ready structured memory.
```

Stronger but still honest:

```text
Stop feeding your AI a pile of chat history. Give it structured memory context.
```

Evidence Identity angle:

```text
Separate repeated memories from independent evidence before they reach the LLM.
```

## 17. Current decision

The current strategic decision is:

```text
SO Memory Engine remains OSS.
SO Extractor Free will provide the public entry path.
SO Extractor Pro will be the commercial input-quality layer.
SO Structural Parser is the long-term proprietary core candidate.
```

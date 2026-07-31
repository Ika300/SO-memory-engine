# Input Schema

SO Extractor Free produces MemoryUnits.

A MemoryUnit is not a final interpretation. It is a structured memory candidate that can be exported toward SO Memory Engine.

## Required fields

- id
- content
- labels
- source_id
- conversation_id
- message_ids

## Relation fields

Each relation contains:

- source
- target
- relation_type
- strength
- directed
- evidence_message_ids

Relation endpoints must reference labels in the same MemoryUnit.

## Important limitation

SO Extractor Free uses transparent rule-based extraction.

It does not correct semantic extraction errors. If labels or relations are poor, SO Memory Engine will preserve and observe poor structure.

```text
bad extraction -> bad MemoryUnits -> weak Context Pack
```

This is not hidden. It is the reason Extractor Pro may later focus on extraction quality, validation, span retention, and canonical memory candidates.
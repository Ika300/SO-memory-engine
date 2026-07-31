# LLM Structured Output Template

SO Extractor Free does not call an LLM, but applications may use an LLM to produce MemoryUnits.

Use strict JSON output and validate before sending anything to SO Memory Engine.

## Rules for an LLM extractor

- Return JSON only.
- Do not invent messages.
- Preserve source_id and message_id.
- Use only allowed relation types accepted by SO Memory Engine.
- Relation endpoints must reference labels.
- Scores must be floats from 0.0 to 1.0.
- If uncertain, omit the relation or lower confidence.
- Do not silently merge memories.
- Keep original evidence references.

## Minimal output shape

```json
{
  "memory_units": [
    {
      "id": "memory_unit_0001",
      "content": "I want to work independently, but income stability worries me.",
      "labels": ["independently", "income", "stability"],
      "relations": [
        {
          "source": "independently",
          "target": "stability",
          "relation_type": "tension",
          "strength": 0.7,
          "directed": false,
          "evidence_message_ids": ["m001"]
        }
      ],
      "source_id": "chat_export_sample",
      "conversation_id": "sample_conversation_001",
      "message_ids": ["m001"],
      "confidence": 0.6
    }
  ]
}
```
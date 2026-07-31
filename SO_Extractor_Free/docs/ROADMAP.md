# Roadmap

SO Extractor is the public entry path into SO Memory Engine.

The project should remain honest about what is free, what is experimental, and what may later become commercial.

## Current Free MVP

Implemented:

- simple JSON conversation loader
- transparent rule-based MemoryUnit extraction
- MemoryUnit validation
- EngineMemory-compatible export
- conversation log demo
- ChatGPT export-like demo
- end-to-end SO Memory Engine demo
- tests

Current status:

```text
Free Extractor MVP: local alpha
External API calls: 0
LLM required: No
Embeddings required: No
```

## Near-term Free goals

Next Free work should focus on adoption, not hidden intelligence:

- clearer MemoryUnit schema
- more input examples
- better validation messages
- optional LLM structured-output examples
- ChatGPT export-like sample and demo
- sample output documentation
- clear Free vs Pro boundary
- CI badge after GitHub publication

## Future Pro direction

SO Extractor Pro, if developed, should not be a locked version of the Free Extractor.

Pro should focus on input quality:

- better relation extraction
- label stabilization
- source/span/evidence retention
- canonical memory candidates
- advanced validation
- Engine-readiness reports
- repair hints
- production templates

## Non-goals for Free Extractor

Free Extractor should not claim:

- perfect natural-language understanding
- production extraction quality
- automatic semantic correction
- hidden ontology merging
- full canonical memory generation

## Strategic boundary

Free Extractor helps people try SO Memory Engine.

Extractor Pro should help real logs become high-quality SO Engine-ready memory.

# Free vs Pro Boundary

SO Extractor Free and a possible SO Extractor Pro should have different jobs.

Free should be easy to try.

Pro should be reliable enough to use in real memory pipelines.

## Free

Free focuses on the first 10 minutes:

- load small conversation logs
- normalize simple message formats
- create transparent rule-based MemoryUnit candidates
- validate the MemoryUnit shape
- export EngineMemory-compatible JSON
- run a small SO Memory Engine demo

Free is allowed to be simple. It should not pretend to be a production parser.

## Pro

Pro should focus on input quality:

- stronger relation extraction
- better label stability
- source span and evidence retention
- Engine-readiness reports
- repair hints
- canonical memory candidates with preserved evidence
- higher-quality Context Pack preparation

## What Pro must not do

Pro must not flatten meaning through silent approximate merging.

If canonical memory candidates are added, they should preserve:

- original message ids
- source ids
- evidence snippets or spans
- uncertainty
- competing interpretations when needed

The commercial value should come from better structure, not from hiding evidence.

## Engine Pro

The open SO Memory Engine should remain the public trust layer.

If paid work later requires Engine improvements, Engine Pro can be considered for:

- stronger Evidence Independence handling
- improved Context Pack quality metadata
- better conflict and unresolved-tension handling
- noise rejection diagnostics
- production-oriented APIs

But Engine changes should follow real Pro needs, not speculative redesign.
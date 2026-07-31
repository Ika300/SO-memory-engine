# Evaluation Principles

SO Memory Engine should be evaluated in a way that can survive skepticism.

The goal is not to design favorable tests. The goal is to learn where the Engine helps, where it does not help, and where the current evidence is still insufficient.

## 1. Do not benchmark the wrong claim

SO Memory Engine is not a vector database, embedding model, LLM, storage layer, chatbot, or natural-language parser.

The public Engine begins after structure exists. It should be evaluated as a structural context construction layer for AI memory.

## 2. Use measured results only

Public documentation must report only results that were actually run.

Do not copy illustrative numbers into README, sales pages, benchmark tables, or release notes unless those numbers came from a reproducible local run.

## 3. Separate behavioral benchmarks from comparative benchmarks

Behavioral benchmarks answer:

> Does the Engine preserve its intended structural memory behavior?

Comparative application benchmarks answer:

> Does an AI application perform better when this Engine is used?

Both are valuable, but they prove different things.

## 4. Include unfavorable and neutral cases

A credible benchmark suite should include:

- cases where SO should help
- cases where SO should not activate anything
- cases where similarity is tempting but structurally wrong
- cases where direction matters
- cases where repeated exposure should not become independent evidence
- cases where SO may not outperform simpler methods

Failure or no-difference results should be preserved when they are real.

## 5. Do not weaken baselines

Comparative tests should not compare SO only against no memory.

Useful baselines include:

- no memory
- recent memory
- keyword search
- simple similarity retrieval
- embedding retrieval when available
- embedding retrieval plus SO

The strongest product position may be combination, not replacement.

## 6. Do not claim natural-language understanding without a parser

The Engine accepts structured memory fragments. It does not claim to turn arbitrary raw text into reliable structure by itself.

Natural-language extraction may be performed by another layer, such as application metadata, rules, LLM structured output, knowledge graphs, external extraction systems, or SO-based extraction systems.

## 7. Preserve the distinction between recurrence and corroboration

Repeated contextual exposure is useful, but it is not the same as independent source evidence.

A benchmark should keep these quantities separate when possible:

- trace fragment count
- unique source count
- contextual recurrence count

## 8. Report limits plainly

Public evaluation should say what the result does not prove.

For the current alpha, behavioral tests do not prove universal application improvement, language understanding, production scalability, or superiority over all retrieval methods.

## 9. Prefer reproducibility over drama

A small benchmark that is easy to run and honest is more valuable than a dramatic benchmark that is hard to inspect.

## 10. Keep the core claim narrow

A good public benchmark question is:

> Given structured memory fragments, can SO Memory Engine build a compact Context Pack that preserves recurrence, return, evidence identity, unresolved tension, and noise rejection?

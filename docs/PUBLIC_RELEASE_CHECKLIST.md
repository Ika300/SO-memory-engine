# Public Release Checklist

SO Memory Engine is not ready for public release until the items below are intentionally resolved.

## Repository readiness

- [ ] Initialize Git repository for `SO_Memory_Engine`.
- [ ] Confirm repository name: `so-memory-engine`.
- [ ] Decide whether the repository is public immediately or private during final polish.
- [ ] Confirm README links after repository creation.

## License

- [x] Decide the public license: Apache-2.0.
- [x] Add a `LICENSE` file.
- [x] Update `pyproject.toml` license metadata.

## Kernel dependency

Current local development uses a sibling-folder bridge:

```text
SO_Memory_Engine
SO_Memory_Kernel
```

Before public release, choose one of these:

1. publish/install SO Memory Kernel as a package dependency;
2. vendor the required Kernel code intentionally;
3. document sibling checkout setup clearly.

Do not silently hide this dependency.

## API stability

- [x] Public imports are defined in `so_memory_engine.__init__`.
- [x] Input validation exists before Kernel execution.
- [x] JSON-safe serialization exists via `to_dict()`.
- [x] Evaluation cases exist.
- [x] Engine tests pass locally.
- [ ] Decide whether `ContextPack.to_prompt_text()` is stable public API or example output.

## Documentation

- [x] README explains what the Engine is and is not.
- [x] Quickstart exists.
- [x] Integration Guide exists.
- [x] Engine API doc exists.
- [x] Evaluation cases doc exists.
- [x] Release Strategy exists.
- [ ] Add a short public example in the future repository description.

## Tests before release

Run from `SO_Memory_Engine`:

```bash
py -3 -m unittest discover -s tests -p '*test*.py' -v
py -3 examples\run_evaluation_cases.py
```

Run from `SO_Memory_Kernel`:

```bash
py -3 -m unittest discover -s tests -p '*test*.py' -v
py -3 benchmarks\run_benchmarks.py
```

## Non-goals to preserve

Do not add these merely for public release:

- LLM calls
- embeddings
- semantic dictionary
- fuzzy semantic merging
- database storage
- web API
- UI
- natural-language parsing

The Engine should remain a narrow memory-context layer.

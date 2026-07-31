# Release Strategy

SO Memory Engine should be released as a separate repository from SO Memory Kernel.

## Repository split

- `so-memory-kernel`: low-level structural memory SDK
- `so-memory-engine`: AI-app-facing memory context layer

This split should remain. The Kernel is the lower-level structural observer. The Engine is the practical integration layer for AI apps.

## Recommended public positioning

Public message:

> Vector memory retrieves what is similar. SO Memory Engine observes what returns.

The Engine should be presented as a structural memory context layer, not as a chatbot, LLM wrapper, vector database, or natural-language parser.

## Free public release

The public repository should include:

- Engine API
- validation
- Context Pack generation
- examples
- evaluation cases
- documentation
- Apache-2.0 license

This gives developers enough to understand and test the idea.

## Future paid/pro boundary

Do not mix paid/pro promises into the first public release.

Future paid materials may include:

- production integration templates
- hosted demos
- advanced evaluation packs
- adapter examples for real apps
- consulting / setup support
- private application scaffolds

The public Engine should remain useful by itself. The paid path should sell convenience, integration, evaluation, and applied packaging rather than hiding the basic idea.

## Kernel dependency strategy\n\nSO Memory Kernel remains a separate public repository, but Engine now declares it as a Git dependency in `pyproject.toml`.\n\nThe default alpha install path is:\n\n```bash\npy -3 -m pip install -e .\n```\n\nThis pulls Kernel from GitHub. Manual sibling-repository setup remains available for local Kernel development or dependency-install failure.\n\nDo not vendor Kernel into Engine unless there is a strong reason. Vendoring blurs the boundary and makes updates harder.

## Alpha release warning

The first Engine release should clearly say:

- alpha prototype
- API may change
- no storage layer
- no LLM calls
- no natural-language parsing
- requires caller-supplied structure
- installs SO Memory Kernel from GitHub by default, with manual local setup available

This honesty is good. It makes the project look serious rather than overhyped.

## Before GitHub publication

Required before publication:

- confirm README is accurate
- confirm LICENSE exists
- run Engine tests
- run evaluation cases
- run Kernel tests
- run Kernel benchmarks
- initialize git repository
- create GitHub repository `Ika300/so-memory-engine`
- push initial commit

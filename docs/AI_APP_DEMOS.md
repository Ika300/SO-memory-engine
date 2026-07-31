# AI App Demo Guide

SO Memory Engine is designed to sit between an AI application and SO Memory Kernel.

It does not generate the final assistant response. It prepares structural memory context that an application may pass to an LLM.

## Demos

### 1. LLM memory engine demo

```bash
py -3 examples\llm_memory_engine_demo.py
```

Shows the basic input-output flow:

```text
current message + past memories
-> SO Memory Engine
-> Context Pack
```

### 2. Chat memory loop demo

```bash
py -3 examples\chat_memory_loop_demo.py
```

Shows how a chat app could use structural memory without treating old messages as generic similar text.

The latest user message remains primary. The Context Pack is optional grounding.

### 3. Agent memory demo

```bash
py -3 examples\agent_memory_demo.py
```

Shows how an agent could notice returning blockers instead of simply retrieving similar tasks.

### 4. Note app memory demo

```bash
py -3 examples\note_memory_demo.py
```

Shows how a note app could surface old unfinished structures that become relevant again.

## What these demos prove

They prove that the Engine can:

- accept current input and past memories
- preserve caller-supplied labels and relations
- call SO Memory Kernel
- produce active memories
- produce returning structures
- produce recurring structures
- produce unresolved tensions
- produce a Context Pack suitable for LLM grounding

## What these demos do not prove

They do not prove:

- automatic natural language understanding
- semantic parsing
- production storage design
- UI design
- LLM response quality
- SaaS readiness

## Boundary

The Engine prepares memory context.
The LLM remains responsible for language generation.
The application remains responsible for storage, parsing, user experience, and permissions.

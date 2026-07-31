# Try Your Own Data

The quickest way to try your own conversation is to copy the sample format.

## 1. Create a JSON file

Example:

```json
{
  "conversation_id": "my_test",
  "messages": [
    {
      "id": "m001",
      "role": "user",
      "text": "I want to build an independent product, but income stability worries me.",
      "source_id": "my_test"
    },
    {
      "id": "m002",
      "role": "assistant",
      "text": "That sounds like a tension between independence and stability."
    },
    {
      "id": "m003",
      "role": "user",
      "text": "I keep returning to freedom, work, money, and fear.",
      "source_id": "my_test"
    }
  ]
}
```

## 2. Run quickstart with your file

```bash
py -3 quickstart.py path\to\my_conversation.json
```

You can also set the current message:

```bash
py -3 quickstart.py path\to\my_conversation.json --current "I am thinking about this again today."
```

## 3. Inspect the output

The quickstart writes:

```text
outputs/free_trial/01_normalized_messages.json
outputs/free_trial/02_memory_units.json
outputs/free_trial/03_validation_report.md
outputs/free_trial/04_engine_memories.json
outputs/free_trial/05_current_memory_unit.json
outputs/free_trial/06_context_pack.json
outputs/free_trial/07_context_pack.txt
outputs/free_trial/08_engine_result.json
```

Start with:

```text
outputs/free_trial/07_context_pack.txt
```

Then inspect the intermediate files if you want to see how the Context Pack was built.

## Important boundary

SO Extractor Free is transparent and simple.

Bad extraction creates bad Engine input.

The Engine preserves supplied structure; it does not silently repair semantic extraction errors.
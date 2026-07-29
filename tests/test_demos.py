from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DemoExecutionTests(unittest.TestCase):
    def run_demo(self, name: str) -> str:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "examples" / name)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        return completed.stdout

    def test_llm_memory_engine_demo_runs(self) -> None:
        output = self.run_demo("llm_memory_engine_demo.py")
        self.assertIn("SO Memory Engine demo", output)
        self.assertIn("STRUCTURAL MEMORY CONTEXT", output)

    def test_chat_memory_loop_demo_runs(self) -> None:
        output = self.run_demo("chat_memory_loop_demo.py")
        self.assertIn("Chat memory loop demo", output)
        self.assertIn("Latest user message", output)

    def test_agent_memory_demo_runs(self) -> None:
        output = self.run_demo("agent_memory_demo.py")
        self.assertIn("Agent memory demo", output)
        self.assertIn("returning blockers", output)

    def test_note_memory_demo_runs(self) -> None:
        output = self.run_demo("note_memory_demo.py")
        self.assertIn("Note app memory demo", output)
        self.assertIn("old structure is active again", output)


if __name__ == "__main__":
    unittest.main()

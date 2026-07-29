from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_demo_outputs(name: str, result: Any, project_root: Path) -> tuple[Path, Path]:
    output_dir = project_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{name}.json"
    text_path = output_dir / f"{name}.txt"
    json_path.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    text_path.write_text(result.context_pack.to_prompt_text(), encoding="utf-8")
    return json_path, text_path

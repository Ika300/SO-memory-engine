from __future__ import annotations

import sys
from pathlib import Path


def ensure_kernel_import_path() -> None:
    """Make sibling SO_Memory_Kernel importable during local development.

    This is a local-development bridge. A future public package should depend on
    an installable `so-memory-kernel` package instead of relying on a sibling
    folder.
    """

    project_root = Path(__file__).resolve().parents[1]
    candidates = [
        project_root.parent / "SO_Memory_Kernel",
        Path.home() / "Desktop" / "SO_Memory_Kernel",
    ]
    for candidate in candidates:
        if (candidate / "so_memory").exists() and str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
            return


ensure_kernel_import_path()

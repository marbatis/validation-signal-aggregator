from __future__ import annotations

import json
from pathlib import Path

from app.schemas import BuildInput


class BuildLoader:
    def __init__(self, root: str = "data/builds"):
        self.root = Path(root)

    def list_build_ids(self) -> list[str]:
        return sorted([path.stem for path in self.root.glob("*.json")])

    def load(self, build_id: str) -> BuildInput:
        payload = json.loads((self.root / f"{build_id}.json").read_text(encoding="utf-8"))
        return BuildInput.model_validate(payload)

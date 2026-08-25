from __future__ import annotations

import re
from pathlib import Path

PROTOCOL_ROOT = Path("src/harn/protocol")
PARAMETER = re.compile(
    r"^(\s*)harn_agents_protocol_version: "
    r"([A-Za-z0-9_]+HarnAgentsProtocolVersion),$",
    re.MULTILINE,
)


def main() -> None:
    changed = 0
    for path in sorted((PROTOCOL_ROOT / "api").rglob("*.py")):
        source = path.read_text()
        normalized = PARAMETER.sub(
            r"\1harn_agents_protocol_version: \2 = "
            r"\2.AGENTS_PROTOCOL_2026_04_25,",
            source,
        )
        if normalized != source:
            path.write_text(normalized)
            changed += 1
    print(f"Normalized protocol defaults in {changed} generated files.")


if __name__ == "__main__":
    main()

"""Placeholder for detecting changes in Clay source material."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = ROOT / "data" / "snapshots"


def main() -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    print("Document change detection is not implemented yet.")


if __name__ == "__main__":
    main()

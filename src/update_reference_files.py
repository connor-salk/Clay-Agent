"""Placeholder for updating Clay reference files."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REFERENCES_DIR = ROOT / "references"


def main() -> None:
    if not REFERENCES_DIR.exists():
        raise FileNotFoundError("references directory is missing")
    print("Reference file update flow is not implemented yet.")


if __name__ == "__main__":
    main()

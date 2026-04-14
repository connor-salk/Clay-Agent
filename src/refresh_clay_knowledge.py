"""Simple entry point for refreshing Clay knowledge files."""

from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "refresh_log.md"


def main() -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    message = f"- Refresh started at {timestamp}\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(message)
    print("Logged Clay knowledge refresh start.")


if __name__ == "__main__":
    main()
